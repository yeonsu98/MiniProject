from django.apps import AppConfig


class MlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ml'

    def ready(self):
        # TODO: Write your codes to run on startup
        import ml.signals
