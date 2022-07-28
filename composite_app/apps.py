from django.apps import AppConfig


class CompositeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'composite_app'
