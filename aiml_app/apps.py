from django.apps import AppConfig

class AimlAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aiml_app'  # Must match your Python import path
    label = 'aiml_app'  # Remove any custom label if present