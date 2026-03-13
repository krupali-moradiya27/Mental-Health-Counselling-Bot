# utils/email_verification.py (recommended)
import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import EmailVerificationModel

def send_verification_email(user):
    otp_code = str(random.randint(100000, 999999))

    EmailVerificationModel.objects.create(
        counsellingchatbot_emailverification_user=user,
        counsellingchatbot_emailverification_code=otp_code,
        counsellingchatbot_emailverification_expire_at=timezone.now() + timedelta(minutes=30)
    )

    subject = "Verify your email address"
    message = f"""
Hi {user.counsellingchatbot_registration_name},

Thank you for registering.

Your email verification code is:

{otp_code}

This code will expire in 30 minutes.

If you didn’t register, please ignore this email.
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.counsellingchatbot_registration_email],
        fail_silently=False,
    )
