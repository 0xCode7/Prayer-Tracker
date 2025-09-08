from django.apps import AppConfig


class AchievementsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'achievements'

    def ready(self):
        # import signals so they're registered
        from . import signals  # noqa: F401