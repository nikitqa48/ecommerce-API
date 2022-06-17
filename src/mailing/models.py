from pyexpat.errors import messages
import pytz
from django.db import models
from datetime import datetime
from django.utils import timezone


class Code(models.Model):
    number = models.IntegerField()


class Tag(models.Model):
    name = models.CharField(max_length=255)


class Filter(models.Model):
    code = models.ForeignKey(Code, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Client(models.Model):
    number = models.IntegerField()
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    timezone = models.CharField(max_length=32, choices=TIMEZONES,default='UTC') 
    tag = models.ManyToManyField(Tag)
    code = models.ForeignKey(Code, related_name = 'operator_code', on_delete=models.CASCADE)


class Message(models.Model):
    start = models.DateTimeField(auto_now_add=True)
    status_choice = (
        ('wait', 'в ожидании'),
        ('start', 'отправка'),
        ('end', 'отправлено')
    )
    status = models.CharField(max_length=255, choices=status_choice)
    clients = models.ManyToManyField(Client)
    text = models.TextField()


class Mailing(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    messages = models.ManyToManyField(Message)
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE, null=True)

    # def save(self, *args, **kwargs):
    #     add.delay(4,4)
    #     current_time = datetime.now().time()
    #     # if current_time > self.start and current_time < self.end:
    #         # print(self.messages.clients[0])
    #     super(Mailing, self).save(*args, **kwargs)


