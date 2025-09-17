from django.shortcuts import render, redirect, get_object_or_404
from dashboardapp.chatbot_rag.retriever import retrieve_similar
from django.http import JsonResponse, HttpResponse
from dashboardapp.models import ChatHistoryModel, ChatSessionModel, PlanModel, SubscriptionModel
from registerapp.models import HealthProfileModel, RegistrationModel
from .chatbot_rag.generate_response import generate_response  
from django.views.decorators.csrf import csrf_exempt
import json 
import uuid
from django.contrib import messages
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.
def dashboardFun(request):
    return render(request, 'dashboard.html')

def chatFun(request):
    user_id = request.session.get("user_id")
    subscription = None
    plan_name = "No Plan"
    if user_id:
        user = get_object_or_404(RegistrationModel, id=user_id)
        subscription = SubscriptionModel.objects.filter(user=user, counselling_chatbot_subscription_is_active=True).first()
        if subscription:
            plan_name = subscription.plan.counselling_chatbot_plan_plan_name
    context = {
        "remaining_token": subscription.counselling_chatbot_subscription_remaining_token if subscription else 0,
        "remaining_word_token": subscription.counselling_chatbot_subscription_remaining_word_token if subscription else 0,
        "plan_name": plan_name,
    }
    print("📝 plan name:", plan_name)

    return render(request, "chat.html", context)

def subscriptionFun(request):
    plans = PlanModel.objects.all()  # Fetch all plans from DB
    return render(request, 'subscription.html', {'plans': plans})

# POST: Chatbot reply (generate + store)
@csrf_exempt
def chatbotresponseFun(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        if not user_id:
            return JsonResponse({"error": "User not authenticated"}, status=401)

        data = json.loads(request.body)
        query = data.get("query", "")
        session_id = data.get("session_id")

        if not query or not session_id:
            return JsonResponse({"error": "Missing data"}, status=400)

        user = get_object_or_404(RegistrationModel, id=user_id)

        session, _ = ChatSessionModel.objects.get_or_create(
            chat_session_id=session_id,
            defaults={
                "user": user,
                "chat_title": "New Chat"
            }
        )

        # Get health profile
        health_profile = HealthProfileModel.objects.filter(counsellingchatbot_health_registration=user).first()
        user_health_data = {}
        if health_profile:
            user_health_data = {
                field.name: getattr(health_profile, field.name)
                for field in HealthProfileModel._meta.fields
            }

        subscription = SubscriptionModel.objects.filter(user=user, counselling_chatbot_subscription_is_active=True).first()
        if not subscription:
            return JsonResponse({"error": "No active subscription found"}, status=403)

        if subscription.counselling_chatbot_subscription_remaining_token <= 0:
            return JsonResponse({"error": "You have no tokens left. Please upgrade your plan."}, status=403)

        if subscription.counselling_chatbot_subscription_remaining_word_token <= 0:
            return JsonResponse({"error": "You have no word tokens left."}, status=403)

        plan_name = subscription.plan.counselling_chatbot_plan_plan_name  

        # Generate response
        response = generate_response(user_id,query, user_health_data)

        # Handle response based on its value
        if isinstance(response, str) and response in ["hi", "ur"]:
            error_message = (
                "⚠️ Hindi language is only available in the Basic and Premium plans."
                if response == "hi"
                else "⚠️ Urdu language is only available in the Premium plan."
            )
            return JsonResponse({
                "error": error_message,
                "response": "",
                "remaining_token": subscription.counselling_chatbot_subscription_remaining_token,
                "remaining_word_token": subscription.counselling_chatbot_subscription_remaining_word_token,
                "plan_name": plan_name
            })

        # Assume response is the actual chatbot response string
        total_words = len(query.split()) + len(response.split())

        # Save chat history
        ChatHistoryModel.objects.create(
            counsellingchatbot_user=user,
            session=session,
            counsellingchatbot_message=query,
            counsellingchatbot_response=response
        )

        # Update subscription tokens
        subscription.counselling_chatbot_subscription_remaining_token = max(0, subscription.counselling_chatbot_subscription_remaining_token - 1)
        subscription.counselling_chatbot_subscription_remaining_word_token = max(0, subscription.counselling_chatbot_subscription_remaining_word_token - total_words)
        subscription.save()

        return JsonResponse({
            "error": None,
            "response": response,
            "remaining_token": subscription.counselling_chatbot_subscription_remaining_token,
            "remaining_word_token": subscription.counselling_chatbot_subscription_remaining_word_token,
            "plan_name": plan_name
        })

    return JsonResponse({"error": "Invalid request", "plan_name": "Unknown"}, status=400)
# GET: Load sessions for sidebar
def getusersessionsFun(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not logged in"}, status=401)

    sessions = ChatSessionModel.objects.filter(user_id=user_id).order_by("-created_at")
    session_list = [
        {"session_id": s.chat_session_id, "title": s.chat_title}
        for s in sessions
    ]
    return JsonResponse({"sessions": session_list})

# GET: Load chat history by session ID
def chathistorybysessionFun(request, session_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not logged in"}, status=401)

    session = get_object_or_404(ChatSessionModel, chat_session_id=session_id, user_id=user_id)

    chats = ChatHistoryModel.objects.filter(
        counsellingchatbot_user_id=user_id,
        session=session
    ).order_by('counsellingchatbot_created_at')

    chat_data = [
        {
            "user_message": chat.counsellingchatbot_message,
            "bot_response": chat.counsellingchatbot_response
        }
        for chat in chats
    ]
    return JsonResponse({"chats": chat_data})

# GET: Create new session
def createnewsessionFun(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not logged in"}, status=401)

    user = get_object_or_404(RegistrationModel, id=user_id)

    # Count existing sessions for title
    count = ChatSessionModel.objects.filter(user=user).count() + 1
    title = f"Chat {count}"

    # Create new session
    new_session = ChatSessionModel.objects.create(
        user=user,
        chat_session_id=str(uuid.uuid4()),
        chat_title=title
    )

    return JsonResponse({"session_id": new_session.chat_session_id})

# POST: Rename session
@csrf_exempt
def renamesessionFun(request, session_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_title = data.get("title")

        if new_title:
            updated = ChatSessionModel.objects.filter(chat_session_id=session_id).update(chat_title=new_title)
            if updated:
                return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"}, status=400)

# DELETE: Delete session and all associated chats
@csrf_exempt
def deletesessionFun(request, session_id):
    if request.method == 'DELETE':
        deleted = ChatSessionModel.objects.filter(chat_session_id=session_id).delete()
        if deleted:
            return JsonResponse({"status": "deleted"})

    return JsonResponse({"status": "error"}, status=400)

def showreceiptFun(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")  # or handle unauthorized access

    subscription = SubscriptionModel.objects.filter(user_id=user_id).order_by("-id").first()
    if not subscription:
        return HttpResponse("No subscription found.")

    plan = subscription.plan  # This gives you access to the PlanModel instance

    context = {
        "user": subscription.user,
        "plan_name": plan.counselling_chatbot_plan_plan_name,
        "price": plan.counselling_chatbot_plan_price,
        "remaining_token": subscription.counselling_chatbot_subscription_remaining_token,
        "remaining_word_token": subscription.counselling_chatbot_subscription_remaining_word_token,
        "subscribed_on": subscription.created_at,
        "status": "Success",  # You can make this dynamic if needed
    }
    return render(request, "receipt.html", context)

def checkoutFun(request):
    if request.method == 'POST':
        plan_id = request.POST.get('plan')
        user_id = request.session.get('user_id')  # assuming you're tracking logged-in user

        if not user_id:
            return JsonResponse({'error': 'User not logged in'}, status=401)

        plan = get_object_or_404(PlanModel, id=plan_id)
        user = get_object_or_404(RegistrationModel, id=user_id)

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': plan.counselling_chatbot_plan_plan_name,
                        },
                        'unit_amount': int(plan.counselling_chatbot_plan_price * 100),  # in paise
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/dashboard/payment/success/'),
                cancel_url=request.build_absolute_uri('/dashboard/payment/cancel/'),
                metadata={
                    "user_id": user.id,
                    "plan_id": plan.id
                }
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def paymentsuccessFun(request):
    return render(request, 'payment_success.html')

def paymentcancelFun(request):
    return render(request, 'payment_cancel.html')

@csrf_exempt
def stripewebhookFun(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get("metadata", {})
        user_id = metadata.get("user_id")
        plan_id = metadata.get("plan_id")

        try:
            user = RegistrationModel.objects.get(id=user_id)
            plan = PlanModel.objects.get(id=plan_id)

            # Get PaymentIntent from session
            payment_intent_id = session.get("payment_intent")
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            # Get payment method from intent
            payment_method_id = payment_intent['payment_method']
            payment_method = stripe.PaymentMethod.retrieve(payment_method_id)

            # Extract card details
            card = payment_method.get("card", {})
            billing_details = payment_method.get("billing_details", {})

            card_holder_name = billing_details.get("name", "Unknown")
            exp_month = card.get("exp_month", 1)
            exp_year = card.get("exp_year", 2099)
            last4 = card.get("last4", "0000")

            SubscriptionModel.objects.create(
                user=user,
                plan=plan,
                counselling_chatbot_subscription_is_active=True,
                counselling_chatbot_subscription_remaining_token=plan.counselling_chatbot_plan_token,
                counselling_chatbot_subscription_remaining_word_token=plan.counselling_chatbot_plan_word_token,
                counselling_chatbot_subscription_card_holder_name=card_holder_name,
                counselling_chatbot_subscription_card_number=f"**** **** **** {last4}",
                counselling_chatbot_subscription_expiry_month=exp_month,
                counselling_chatbot_subscription_expiry_year=exp_year,
            )
            print(f" Subscription saved with card ending in {last4}")

        except Exception as e:
            print("⚠️ Error saving subscription:", e)
        return HttpResponse(status=200)


# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)

#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         metadata = session.get("metadata", {})

#         user_id = metadata.get("user_id")
#         plan_id = metadata.get("plan_id")

#         try:
#             user = RegistrationModel.objects.get(id=user_id)
#             plan = PlanModel.objects.get(id=plan_id)

#             SubscriptionModel.objects.create(
#                 user=user,
#                 plan=plan,
#                 counselling_chatbot_subscription_remaining_token=plan.counselling_chatbot_plan_token,
#                 counselling_chatbot_subscription_remaining_word_token=plan.counselling_chatbot_plan_word_limit,
#                 counselling_chatbot_subscription_card_holder_name=session.get("customer_details", {}).get("name", ""),
#                 counselling_chatbot_subscription_card_number="**** **** **** 4242",  # just a masked default
#                 counselling_chatbot_subscription_expiry_month=1,  # Can't be fetched from Stripe unless using SetupIntent
#                 counselling_chatbot_subscription_expiry_year=2099,
#             )
#             print("✅ Subscription saved for user:", user)
#         except (RegistrationModel.DoesNotExist, PlanModel.DoesNotExist):
#             return HttpResponse(status=404)

#     return HttpResponse(status=200)


# @csrf_exempt
# def subscribeuserFun(request):
#     if request.method == "POST":
#         user_id = request.session.get("user_id")
#         if not user_id:
#             messages.error(request, "Please log in to subscribe.")
#             return redirect('subscribeuserPage')

#         try:
#             user = RegistrationModel.objects.get(id=user_id)
#             plan_id = request.POST.get("plan")
#             plan = PlanModel.objects.get(id=plan_id)

#             # Create the subscription record
#             SubscriptionModel.objects.create(
#                 user=user,
#                 plan=plan,
#                 counselling_chatbot_subscription_remaining_token=plan.counselling_chatbot_plan_token,
#                 counselling_chatbot_subscription_remaining_word_token=plan.counselling_chatbot_plan_word_token,
#                 counselling_chatbot_subscription_card_holder_name=request.POST.get("card_name"),
#                 counselling_chatbot_subscription_card_number=request.POST.get("card_number"),
#                 counselling_chatbot_subscription_expiry_month=request.POST.get("exp_month"),
#                 counselling_chatbot_subscription_expiry_year=request.POST.get("exp_year")
#             )

#             messages.success(request, "Subscription successful!")
#             return redirect("showreceiptPage")  # or wherever you want to go

#         except PlanModel.DoesNotExist:
#             messages.error(request, "Invalid plan selected.")
#         except Exception as e:
#             messages.error(request, f"Something went wrong: {str(e)}")

#     return redirect('subscribeuserPage')