from django.db import models
from registerapp.models import RegistrationModel  # Import your user model

class ChatSessionModel(models.Model):
    user = models.ForeignKey(RegistrationModel, on_delete=models.CASCADE, related_name="user_sessions")
    chat_session_id = models.CharField(max_length=100, unique=True)
    chat_title = models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "counsellingchatbot_chat_session_tb"

    def __str__(self):
        return f"{self.chat_title} ({self.user.counsellingchatbot_registration_name})"

class ChatHistoryModel(models.Model):

    counsellingchatbot_user = models.ForeignKey(
        RegistrationModel,
        on_delete=models.CASCADE,
        related_name='chats'
    )

    session = models.ForeignKey(
        ChatSessionModel,
        on_delete=models.CASCADE,
        related_name="chat_messages",
        null=True  # <-- Add this
    )

    counsellingchatbot_message = models.TextField()
    counsellingchatbot_response = models.TextField()
    counsellingchatbot_word_count = models.IntegerField(default=0)
    counsellingchatbot_token_count = models.IntegerField(default=0)
    counsellingchatbot_created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'counsellingchatbot_chat_tb'

    def __str__(self):
        return f'chat for {self.counsellingchatbot_user.counsellingchatbot_registration_name} in session {self.session.chat_title}'

class PlanModel(models.Model):
    counselling_chatbot_plan_plan_name = models.CharField(max_length=50, unique=True)
    counselling_chatbot_plan_description = models.TextField()
    counselling_chatbot_plan_price = models.DecimalField(max_digits=8, decimal_places=2)  # e.g. 99999.99
    counselling_chatbot_plan_token = models.IntegerField(help_text="Message token limit for the plan")
    counselling_chatbot_plan_word_token = models.IntegerField(help_text="Word token limit for the plan")

    class Meta:
        db_table = 'counselling_chatbot_plan_tb'

    def __str__(self):
        return self.counselling_chatbot_plan_plan_name

class SubscriptionModel(models.Model):
    user = models.ForeignKey(RegistrationModel, on_delete=models.CASCADE)
    plan = models.ForeignKey(PlanModel, on_delete=models.CASCADE)
    counselling_chatbot_subscription_is_active = models.BooleanField(default=True)
    counselling_chatbot_subscription_remaining_token = models.IntegerField()
    counselling_chatbot_subscription_remaining_word_token = models.IntegerField()
    counselling_chatbot_subscription_card_holder_name = models.CharField(max_length=100)
    counselling_chatbot_subscription_card_number = models.CharField(max_length=20)  # you can mask it in views/templates
    counselling_chatbot_subscription_expiry_month = models.IntegerField()
    counselling_chatbot_subscription_expiry_year = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'counselling_chatbot_subscription_tb'

    def __str__(self):
        return f"{self.user} - {self.plan.counselling_chatbot_plan_plan_name}"
