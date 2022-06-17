from django.contrib import admin
from .models import BasketLine as Line, Basket
# Register your models here.


class LineInline(admin.TabularInline):
    model = Line
    readonly_fields = ('product',)

@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    list_display = ('id', 'basket', 'product', 'quantity', 'date_created')
    # readonly_fields = ('basket',  'product', 'quantity')

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id',  'status', 'num_lines', 'date_created', 'date_submitted',)
    # readonly_fields = ('owner', 'date_merged', 'date_submitted', )
    inlines = [LineInline]