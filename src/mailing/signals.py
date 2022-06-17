from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Mailing, Client
from .tasks import add, printer
from django_celery_beat.models import CrontabSchedule, PeriodicTask, IntervalSchedule

def send():
    print("send email!")

@receiver(post_save, sender=Mailing)
def send_email(instance, **kwargs):
    print('start signal')
    # send()
    # clients = Client.objects.filter(code=instance.filter.code, tag=instance.filter.tag)
    # print(clients)
    # printer.delay()
    schedule, _ = CrontabSchedule.objects.get_or_create(
    minute='1',
    hour='*',
    day_of_week='*',
    day_of_month='*',
    month_of_year='*',
    )
    PeriodicTask.objects.create(
    crontab=schedule,
    name='notification2',
    task='src.mailing.tasks.printer',
    )
    printer.delay()

    