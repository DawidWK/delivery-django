from django.contrib import admin
from .models import Order

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('date_order',)

admin.site.register(Order, OrderAdmin)
