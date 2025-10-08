from django.contrib import admin
from .models import PlanModel
@admin.register(PlanModel)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        'counselling_chatbot_plan_plan_name',
        'counselling_chatbot_plan_description',
        'counselling_chatbot_plan_price',
        'counselling_chatbot_plan_token',
        'counselling_chatbot_plan_word_token'
    )