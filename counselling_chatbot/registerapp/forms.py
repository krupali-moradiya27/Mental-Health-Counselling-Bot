from django import forms
from .models import RegistrationModel, HealthProfileModel
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator

class RegistrationForm(forms.ModelForm):
    counsellingchatbot_registration_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        max_length=128,
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        max_length=128,
        label='Confirm Password'
    )
    counsellingchatbot_registration_terms_accepted = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must accept the terms & conditions.'}
    )

    class Meta:
        model = RegistrationModel
        fields = [
            'counsellingchatbot_registration_name',
            'counsellingchatbot_registration_email',
            'counsellingchatbot_registration_password',
            'confirm_password',
            'counsellingchatbot_registration_terms_accepted'
        ]
        widgets = {
            'counsellingchatbot_registration_name': forms.TextInput(attrs={'class': 'form-control'}),
            'counsellingchatbot_registration_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'counsellingchatbot_registration_terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_counsellingchatbot_registration_name(self):
        name = self.cleaned_data.get('counsellingchatbot_registration_name')
        if not name:
            raise ValidationError("Name is required.")
        if not re.match(r'^[A-Za-z]{2,}$', name):
            raise ValidationError("Name must be at least 2 letters and contain only letters.")
        return name

    def clean_counsellingchatbot_registration_email(self):
        email = self.cleaned_data.get('counsellingchatbot_registration_email')
        if not email:
            raise ValidationError("Email is required.")
        if not email.endswith('@gmail.com'):
            raise ValidationError("Only Gmail addresses are allowed (e.g., example@gmail.com).")
        if RegistrationModel.objects.filter(counsellingchatbot_registration_email=email).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_counsellingchatbot_registration_password(self):
        password = self.cleaned_data.get('counsellingchatbot_registration_password')
        if not password:
            raise ValidationError("Password is required.")
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            raise ValidationError(
                "Password must be at least 8 characters long, include 1 uppercase letter, 1 number, and 1 special character."
            )
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("counsellingchatbot_registration_password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and not confirm_password:
            self.add_error('confirm_password', "Please confirm your password.")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['counsellingchatbot_registration_password']:
            user.counsellingchatbot_registration_password = make_password(
                self.cleaned_data['counsellingchatbot_registration_password'],
                hasher='argon2'
            )
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    counsellingchatbot_registration_email = forms.EmailField(label="Email")
    counsellingchatbot_registration_password = forms.CharField(widget=forms.PasswordInput, label="Password")

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = RegistrationModel
        fields = [
            'counsellingchatbot_registration_name',
            'counsellingchatbot_registration_email',
            'counsellingchatbot_registration_contact_phone',
            'counsellingchatbot_registration_language',
            'counsellingchatbot_registration_avatar',
        ]
        widgets = {
            'counsellingchatbot_registration_email': forms.EmailInput(attrs={'readonly': 'readonly'}),
            'counsellingchatbot_registration_name': forms.TextInput(),
        }

class HealthProfileForm(forms.ModelForm):
    counsellingchatbot_health_sleep_hours = forms.IntegerField(required=False, validators=[MinValueValidator(0)])
    class Meta:
        model = HealthProfileModel
        fields = [
            'counsellingchatbot_health_sleep_hours',
            'counsellingchatbot_health_sleep_trouble',
            'counsellingchatbot_health_isolated',
            'counsellingchatbot_health_support_system',
            'counsellingchatbot_health_exercise_frequency',
            'counsellingchatbot_health_negative_thoughts',
            'counsellingchatbot_health_coping_mechanisms',
            'counsellingchatbot_health_common_negative_thoughts',
            'counsellingchatbot_health_cognitive_load',
            'counsellingchatbot_health_dietary_habits',
            'counsellingchatbot_health_triggers',
            'counsellingchatbot_health_stressors',
            'counsellingchatbot_health_social_pref',
            'counsellingchatbot_health_mindfulness_interest',
            'counsellingchatbot_health_mental_history',
            'counsellingchatbot_health_therapy_experience',
            'counsellingchatbot_health_meditation_experience',
            'counsellingchatbot_health_energy_level',
            'counsellingchatbot_health_stress_level',
            'counsellingchatbot_health_doctor_conversation'
        ]
        widgets = {
            'counsellingchatbot_health_doctor_conversation': forms.Textarea(attrs={'rows': 3}),
        }
