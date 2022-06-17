from django.contrib import admin
from .models import Mailing, Message, Filter, Code, Tag, Client

@admin.register(Mailing)

class AdminMailing(admin.ModelAdmin):
    class Meta:
        model = Mailing
        fields = '__all__'

@admin.register(Tag)

class AdminTag(admin.ModelAdmin):
    class Meta:
        model = Tag
        fields = '__all__'

@admin.register(Code)

class AdminCode(admin.ModelAdmin):
    class Meta:
        model = Code
        fields = '__all__'

@admin.register(Filter)

class AdminFilter(admin.ModelAdmin):
    class Meta:
        model = Filter
        fields = '__all__'

@admin.register(Message)
class AdminMessage(admin.ModelAdmin):
    class Meta:
        model = Message
        fields = '__all__'

@admin.register(Client)
class AdminClient(admin.ModelAdmin):
    class Meta:
        model = Client
        fields = '__all__'