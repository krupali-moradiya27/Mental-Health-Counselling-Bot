from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

class RegistrationModel(models.Model):
    counsellingchatbot_registration_name = models.CharField(max_length=150, null=True, blank=True, default=None)
    counsellingchatbot_registration_email = models.EmailField(unique=True, null=True, blank=True, default=None)
    counsellingchatbot_registration_password = models.CharField(max_length=128, null=True, blank=True, default=None)
    counsellingchatbot_registration_terms_accepted = models.BooleanField(default=False)
    counsellingchatbot_registration_contact_phone = models.CharField(max_length=20, null=True, blank=True, default=None)  
    counsellingchatbot_registration_language = models.CharField(max_length=50, null=True, blank=True, default=None)
    counsellingchatbot_registration_avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default=None)
    counsellingchatbot_registration_created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'counsellingchatbot_registration_tb'

    def __str__(self):
        return str(self.counsellingchatbot_registration_email)

class HealthProfileModel(models.Model):
    # Link to the registration model
    counsellingchatbot_health_registration = models.ForeignKey(
        'RegistrationModel', 
        on_delete=models.CASCADE, 
        related_name='health_profiles'                              
    )
    
    counsellingchatbot_health_sleep_hours = models.IntegerField(null=True, blank=True, default=None, validators=[MinValueValidator(0)])
    counsellingchatbot_health_sleep_trouble = models.CharField(max_length=20, null=True, blank=True, default=None)
    counsellingchatbot_health_isolated = models.CharField(max_length=20, null=True, blank=True, default=None)
    counsellingchatbot_health_support_system = models.CharField(max_length=20, null=True, blank=True, default=None)
    counsellingchatbot_health_exercise_frequency = models.CharField(max_length=50, null=True, blank=True, default=None)
    counsellingchatbot_health_negative_thoughts = models.CharField(max_length=20, null=True, blank=True, default=None)
    counsellingchatbot_health_coping_mechanisms = models.CharField(max_length=255, null=True, blank=True, default=None)
    counsellingchatbot_health_common_negative_thoughts = models.CharField(max_length=255, null=True, blank=True, default=None)
    counsellingchatbot_health_cognitive_load = models.CharField(max_length=20, null=True, blank=True, default=None)
    counsellingchatbot_health_dietary_habits = models.CharField(max_length=255, null=True, blank=True, default=None)
    counsellingchatbot_health_triggers = models.CharField(max_length=255, null=True, blank=True, default=None)
    counsellingchatbot_health_stressors = models.CharField(max_length=255, null=True, blank=True, default=None)
    counsellingchatbot_health_social_pref = models.CharField(max_length=20, null=True, blank=True, default=None)
    counsellingchatbot_health_mindfulness_interest = models.CharField(max_length=20, null=True, blank=True, default=None)
    counsellingchatbot_health_mental_history = models.CharField(max_length=255, null=True, blank=True, default=None)
    counsellingchatbot_health_therapy_experience = models.CharField(max_length=10, null=True, blank=True, default=None)
    counsellingchatbot_health_meditation_experience = models.CharField(max_length=10, null=True, blank=True, default=None)
    counsellingchatbot_health_energy_level = models.IntegerField(null=True, blank=True, default=None)
    counsellingchatbot_health_stress_level = models.IntegerField(null=True, blank=True, default=None)
    counsellingchatbot_health_doctor_conversation = models.TextField(null=True, blank=True, default=None)
    counsellingchatbot_health_created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'counsellingchatbot_healthprofile_tb'

    def __str__(self):
        return f'Health Profile for {self.counsellingchatbot_health_registration}'

class EmailVerificationModel(models.Model):
    counsellingchatbot_emailverification_user = models.ForeignKey(
        'RegistrationModel',
        on_delete=models.CASCADE,
        related_name='email_verifications'
    )
    counsellingchatbot_emailverification_code = models.CharField(max_length=100)
    counsellingchatbot_emailverification_created_at = models.DateTimeField(default=timezone.now)
    counsellingchatbot_emailverification_expire_at = models.DateTimeField()
    counsellingchatbot_emailverification_is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'counsellingchatbot_emailverification_tb'

    def __str__(self):
        return f"Email verification for {self.counsellingchatbot_emailverification_user}"

    @staticmethod
    def get_expiry_time(minutes=30):
        return timezone.now() + timedelta(minutes=minutes)
