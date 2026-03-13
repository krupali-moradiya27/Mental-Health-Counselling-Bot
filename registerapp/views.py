from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .mail_verification import send_verification_email
from .forms import RegistrationForm, HealthProfileForm
from .models import EmailVerificationModel, RegistrationModel, HealthProfileModel
from argon2 import PasswordHasher, exceptions as argon2_exceptions
from argon2.exceptions import Argon2Error, VerifyMismatchError
ph = PasswordHasher()

def registerFun(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.counsellingchatbot_registration_is_email_verified = False
            user.save()

            # SEND OTP + STORE IN EmailVerificationModel
            send_verification_email(user)

            # STORE USER ID IN SESSION (SAFE)
            request.session['verify_user_id'] = user.id

            messages.success(
                request,
                "Registration successful! Please verify your email."
            )

            return redirect('emailVerificationPage')

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def verifyEmailFun(request):
    user_id = request.session.get('verify_user_id')

    if not user_id:
        messages.error(request, "Session expired. Please register again.")
        return redirect('registerPage')

    user = get_object_or_404(RegistrationModel, id=user_id)

    return render(
        request,
        'email_verification.html',
        {
            'email': user.counsellingchatbot_registration_email
        }
    )

def verifyOtpFun(request):
    if request.method != "POST":
        return redirect('registerPage')

    otp = request.POST.get('verification_code')
    user_id = request.session.get('verify_user_id')

    if not otp or not user_id:
        messages.error(request, "Session expired.")
        return redirect('registerPage')

    user = get_object_or_404(RegistrationModel, id=user_id)

    try:
        verification = EmailVerificationModel.objects.filter(
            counsellingchatbot_emailverification_user=user,
            counsellingchatbot_emailverification_code=otp,
            counsellingchatbot_emailverification_is_verified=False
        ).latest('counsellingchatbot_emailverification_created_at')

    except EmailVerificationModel.DoesNotExist:
        messages.error(request, "Invalid verification code.")
        return redirect('emailVerificationPage')

    # CHECK EXPIRY
    if verification.counsellingchatbot_emailverification_expire_at < timezone.now():
        messages.error(request, "Verification code expired.")
        return redirect('emailVerificationPage')

    # MARK VERIFIED
    verification.counsellingchatbot_emailverification_is_verified = True
    verification.save()

    user.counsellingchatbot_registration_is_email_verified = True
    user.save()

    # CLEAR SESSION
    del request.session['verify_user_id']

    messages.success(request, "Email verified successfully. Please login.")
    return redirect('loginPage')

def resendVerificationCode(request):
    user_id = request.session.get('verify_user_id')

    if not user_id:
        messages.error(request, "Session expired. Please register again.")
        return redirect('registerPage')

    user = get_object_or_404(RegistrationModel, id=user_id)

    # GET LATEST EMAIL VERIFICATION RECORD
    verification = (
        EmailVerificationModel.objects
        .filter(counsellingchatbot_emailverification_user=user)
        .order_by('-counsellingchatbot_emailverification_created_at')
        .first()
    )

    # Already verified
    if verification and verification.counsellingchatbot_emailverification_is_verified:
        messages.info(request, "Email already verified.")
        return redirect('loginPage')

    # SEND NEW OTP (your existing function should create a new row)
    send_verification_email(user)

    messages.success(request, "Verification code resent successfully.")
    return redirect('emailVerificationPage')

def loginFun(request):
    error = None

    if request.method == "POST":
        email = request.POST.get('counsellingchatbot_registration_email')
        password = request.POST.get('counsellingchatbot_registration_password')

        if not email or not password:
            error = "All fields are required"
            return render(request, 'login.html', {'error': error})

        try:
            user = RegistrationModel.objects.get(
                counsellingchatbot_registration_email=email
            )

            # EMAIL VERIFICATION CHECK (USING EmailVerificationModel)
            is_verified = EmailVerificationModel.objects.filter(
                counsellingchatbot_emailverification_user=user,
                counsellingchatbot_emailverification_is_verified=True
            ).exists()

            if not is_verified:
                error = "Please verify your email before logging in."
                return render(request, 'login.html', {'error': error})

            # PASSWORD CHECK
            if not check_password(
                password,
                user.counsellingchatbot_registration_password
            ):
                error = "Invalid email or password"
                return render(request, 'login.html', {'error': error})

            # LOGIN SUCCESS
            request.session['user_id'] = user.id
            messages.success(request, "Login successful!")
            return redirect('dashboardPage')

        except RegistrationModel.DoesNotExist:
            error = "Invalid email or password"

    return render(request, 'login.html', {'error': error})

def editProfileFun(request):
    user_id = request.session['user_id']
    user = get_object_or_404(RegistrationModel, id=user_id)
    if HealthProfileModel.objects.filter(counsellingchatbot_health_registration=user).exists():

        healthdata = HealthProfileModel.objects.get(counsellingchatbot_health_registration=user)
    else:
        healthdata= None
    if request.method == "POST":
        user.counsellingchatbot_registration_name = request.POST.get("counsellingchatbot_registration_name")
        user.counsellingchatbot_registration_email = request.POST.get("counsellingchatbot_registration_email")
        user.counsellingchatbot_registration_contact_phone = request.POST.get("counsellingchatbot_registration_contact_phone")
        user.counsellingchatbot_registration_language = request.POST.get("counsellingchatbot_registration_language")

        if "counsellingchatbot_registration_avatar" in request.FILES:
            user.counsellingchatbot_registration_avatar = request.FILES["counsellingchatbot_registration_avatar"]

        user.save()
        return redirect("profilePage")  # Change this to your desired redirect URL

    return render(request, "editprofile.html", {"user": user, "health_profile": healthdata} )

def profileFun(request):
    user_id = request.session['user_id']
    user = get_object_or_404(RegistrationModel, id=user_id)

    # Fetch health profile for the logged-in user
    try:
        health_profile = HealthProfileModel.objects.get(
            counsellingchatbot_health_registration=user
        )
    except HealthProfileModel.DoesNotExist:
        health_profile = None

    return render(request, "profile.html", {
        "user": user,
        "health_profile": health_profile
    })

def healthprofileFun(request):
    if not request.session.get('user_id'):
        messages.error(request, "Session expired, please login again.")
        return redirect('loginPage')

    user_id = request.session['user_id']
    user = get_object_or_404(RegistrationModel, id=user_id)

    # Fetch or create health profile for the user
    health_profile, created = HealthProfileModel.objects.get_or_create(
        counsellingchatbot_health_registration=user
    )

    if request.method == "POST":
        # Collect form data via request.POST.get()
        health_profile.counsellingchatbot_health_sleep_hours = request.POST.get('counsellingchatbot_health_sleep_hours', "")
        health_profile.counsellingchatbot_health_sleep_trouble = request.POST.get('counsellingchatbot_health_sleep_trouble', "")
        health_profile.counsellingchatbot_health_isolated = request.POST.get('counsellingchatbot_health_isolated', "")
        health_profile.counsellingchatbot_health_support_system = request.POST.get('counsellingchatbot_health_support_system', "")
        health_profile.counsellingchatbot_health_exercise_frequency = request.POST.get('counsellingchatbot_health_exercise_frequency', "")
        health_profile.counsellingchatbot_health_negative_thoughts = request.POST.get('counsellingchatbot_health_negative_thoughts', "")
        health_profile.counsellingchatbot_health_coping_mechanisms = request.POST.get('counsellingchatbot_health_coping_mechanisms', "")
        health_profile.counsellingchatbot_health_common_negative_thoughts = request.POST.get('counsellingchatbot_health_common_negative_thoughts', "")
        health_profile.counsellingchatbot_health_cognitive_load = request.POST.get('counsellingchatbot_health_cognitive_load', "")
        health_profile.counsellingchatbot_health_dietary_habits = request.POST.get('counsellingchatbot_health_dietary_habits', "")
        health_profile.counsellingchatbot_health_triggers = request.POST.get('counsellingchatbot_health_triggers', "")
        health_profile.counsellingchatbot_health_stressors = request.POST.get('counsellingchatbot_health_stressors', "")
        health_profile.counsellingchatbot_health_social_pref = request.POST.get('counsellingchatbot_health_social_pref', "")
        health_profile.counsellingchatbot_health_mindfulness_interest = request.POST.get('counsellingchatbot_health_mindfulness_interest', "")
        health_profile.counsellingchatbot_health_mental_history = request.POST.get('counsellingchatbot_health_mental_history', "")
        health_profile.counsellingchatbot_health_therapy_experience = request.POST.get('counsellingchatbot_health_therapy_experience', "")
        health_profile.counsellingchatbot_health_meditation_experience = request.POST.get('counsellingchatbot_health_meditation_experience', "")
        health_profile.counsellingchatbot_health_energy_level = request.POST.get('counsellingchatbot_health_energy_level', "")
        health_profile.counsellingchatbot_health_stress_level = request.POST.get('counsellingchatbot_health_stress_level', "")
        health_profile.counsellingchatbot_health_doctor_conversation = request.POST.get('counsellingchatbot_health_doctor_conversation', "")

        # Save to DB
        health_profile.save()

        messages.success(request, "Health profile updated successfully!")
        return redirect('profilePage')  # redirect where needed

    return render(request, "editprofile.html", {
        'user': user,
        'health_profile': health_profile
    })

def changepasswordFun(request):

    if request.method == "POST":

        current_password = request.POST.get('counsellingchatbot_registration_currentpassword')
        new_password = request.POST.get('counsellingchatbot_registration_newpassword')
        confirm_password = request.POST.get('counsellingchatbot_registration_confirmnewpassword')

        # Check if new passwords match
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.", extra_tags="changepassword")
            return redirect('editprofilePage')

        user_id = request.session.get('user_id')

        if not user_id:
            messages.error(request, "Session expired. Please login again.")
            return redirect('loginPage')

        # Fetch user
        user = get_object_or_404(RegistrationModel, id=user_id)

        # Verify current password (same as login)
        if not check_password(current_password, user.counsellingchatbot_registration_password):
            messages.error(request, "Current password is incorrect.", extra_tags="changepassword")
            return redirect('editprofilePage')

        # Hash and save new password (same as registration)
        user.counsellingchatbot_registration_password = make_password(
            new_password,
            hasher='argon2'
        )
        user.save()

        messages.success(request, "Password updated successfully.", extra_tags="changepassword")
        return redirect('editprofilePage')

    return render(request, 'editprofile.html')

def logoutFun(request):
    request.session.flush()  # This clears the session
    messages.success(request, "You have been logged out successfully.")
    return redirect('homePage')  # Redirect to your login page

