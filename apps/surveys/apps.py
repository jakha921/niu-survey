from django.apps import AppConfig


class SurveysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.surveys'
    verbose_name = 'Опросы'
    
    def ready(self):
        """Импорт сигналов при готовности приложения"""
        pass 