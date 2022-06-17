from celery import shared_task
from celery.task import periodic_task
from celery.schedules import crontab
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Mailing
from django_celery_beat.models import CrontabSchedule, PeriodicTask

@shared_task
def add():
    print('start task')


@periodic_task(run_every=crontab(minute=26, hour='7,19'))
def printer():
    print('printer')

@shared_task(name="repeat_order_make")
def repeat_order_make():
    print(PeriodicTask.objects.all())
	# order = Order.objects.get(pk=order_id)
	# if order.status != '0':
	# 	print('Статус получен!')
	# 	task = PeriodicTask.objects.get(name='Repeat order {}'.format(order_id))
	# 	task.enabled = False
	# 	task.save()
	# else:
	# 	# Необходимая логика при повторной отправке заказа
	# 	print('Я должна повторно оформлять заказ каждые 10 секунд')