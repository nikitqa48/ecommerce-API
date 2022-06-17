from django.apps import AppConfig


class MailConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.mailing'
    def ready(self):
        import src.mailing.signals
        # from .tasks import repeat_order_make
        # repeat_order_make.delay()
