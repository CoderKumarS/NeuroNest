from django.apps import AppConfig


class TutorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tutor'
    verbose_name = 'AI Tutor'
    
    def ready(self):
        # Import signals if any
        try:
            import tutor.signals
        except ImportError:
            pass