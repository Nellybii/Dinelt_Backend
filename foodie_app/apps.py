from django.apps import AppConfig


class FoodieAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foodie_app'

    def ready(self):
        import foodie_app.signals
