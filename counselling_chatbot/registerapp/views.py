from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegistrationForm, HealthProfileForm
from .models import RegistrationModel, HealthProfileModel
from argon2 import PasswordHasher, exceptions as argon2_exceptions
from argon2.exceptions import VerifyMismatchError
ph = PasswordHasher()

def registerFun(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            try:
                # Hash the password before saving it
                hashed_password = ph.hash(form.cleaned_data['counsellingchatbot_registration_password'])

                # Save user data with hashed password
                user = RegistrationModel.objects.create(
                    counsellingchatbot_registration_name=form.cleaned_data['counsellingchatbot_registration_name'],
                    counsellingchatbot_registration_email=form.cleaned_data['counsellingchatbot_registration_email'],
                    counsellingchatbot_registration_password=hashed_password,  # Store hashed password
                    counsellingchatbot_registration_terms_accepted=form.cleaned_data['counsellingchatbot_registration_terms_accepted']
                )
                
                messages.success(request, "Registration successful! You can now log in.")
                return redirect('loginPage')

            except Argon2Error:
                messages.error(request, "Error hashing password. Please try again.")
        
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def loginFun(request):
    error = None
    if request.method == "POST":
        email = request.POST.get('counsellingchatbot_registration_email')
        password = request.POST.get('counsellingchatbot_registration_password')

        if email and password:
            try:
                user = RegistrationModel.objects.get(counsellingchatbot_registration_email=email)
                try:
                    ph.verify(user.counsellingchatbot_registration_password, password)

                    # Optional rehashing
                    if ph.check_needs_rehash(user.counsellingchatbot_registration_password):
                        user.counsellingchatbot_registration_password = ph.hash(password)
                        user.save()

                    request.session['user_id'] = user.id
                    messages.success(request, "Login successful!")
                    return redirect('dashboardPage')  # Change 'dash' to your actual home/dashboard URL name
                    
                except argon2_exceptions.VerifyMismatchError:
                    error = "Invalid email or password"
                except argon2_exceptions.InvalidHashError:
                    error = "Stored password hash is invalid. Please reset your password."

            except RegistrationModel.DoesNotExist:
                error = "Invalid email or password"
        else:
            error = "All fields are required"

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

        # ✅ Check if new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.", extra_tags="changepassword")
            return redirect('editprofilePage')

        user_id = request.session.get('user_id')

        if user_id:
            user = get_object_or_404(RegistrationModel, id=user_id)  # Fetch user

            # ✅ Verify current password
            try:
                ph.verify(user.counsellingchatbot_registration_password, current_password)

                # ✅ If verified, hash and update new password
                user.counsellingchatbot_registration_password = ph.hash(new_password)
                user.save()

                messages.success(request, "Password updated successfully.", extra_tags="changepassword")
                return redirect('editprofilePage')  # Stay on edit profile page

            except VerifyMismatchError:
                messages.error(request, "Current password is incorrect.", extra_tags="changepassword")

    return render(request, 'editprofile.html')

def logoutFun(request):
    request.session.flush()  # This clears the session
    messages.success(request, "You have been logged out successfully.")
    return redirect('homePage')  # Redirect to your login page

