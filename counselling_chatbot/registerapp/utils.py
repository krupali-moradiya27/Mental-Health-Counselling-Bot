from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured

def insert_data(model_name, data):
    """
    Dynamically insert data into any Django model by passing the model name and data.

    Args:
        model_name (str): The name of the model (case-sensitive).
        data (dict): A dictionary of field names and their corresponding values.

    Returns:
        str: Success or error message.
    """
    try:
        # Get the model dynamically
        model = apps.get_model('registerapp', model_name)  # Change 'registerapp' to your app name
        if not model:
            return f"Error: Model '{model_name}' not found."

        # Create and save the model instance
        instance = model.objects.create(**data)
        return f"{model_name} record added successfully! ID: {instance.id}"

    except ImproperlyConfigured:
        return "Error: Django model configuration is incorrect."
    except ObjectDoesNotExist:
        return f"Error: Model '{model_name}' does not exist."
    except Exception as e:
        return f"Error: {str(e)}"
