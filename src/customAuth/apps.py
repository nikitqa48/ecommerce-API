from django.apps import AppConfig


class CustomauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = 'Авторизация'
    name = 'src.customAuth'
