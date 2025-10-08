from dashboardapp.models import HealthProfileModel

def get_user_health_profile(user_id):
    """Retrieve and format the user's health profile for AI input."""
    try:
        profile = HealthProfileModel.objects.get(counsellingchatbot_health_registration=user_id)
        user_health_info = {
            "sleep_hours": profile.counsellingchatbot_health_sleep_hours,
            "sleep_trouble": profile.counsellingchatbot_health_sleep_trouble,
            "exercise_frequency": profile.counsellingchatbot_health_exercise_frequency,
            "stress_level": profile.counsellingchatbot_health_stress_level,
            "negative_thoughts": profile.counsellingchatbot_health_negative_thoughts,
            "coping_mechanisms": profile.counsellingchatbot_health_coping_mechanisms,
            "mental_history": profile.counsellingchatbot_health_mental_history,
        }
    except HealthProfileModel.DoesNotExist:
        user_health_info = {"error": "No health data available"}

    return user_health_info
