from django.db import models
from decimal import *
from django.utils import timezone
import datetime

# Create your models here.

class Order(models.Model):
    MENU = (
        ('PIZZA', 'pizza'),
        ('SOUP', 'soup'),
        ('FRIES', 'fries'),
        ('BURGER', 'burger'),
    )

    city = models.CharField(max_length=255)
    product = models.CharField(max_length=6, choices=MENU)
    queue_positon = models.IntegerField(default=0)
    date_order = models.DateTimeField(auto_now_add=True)
    wait_time = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return f'Order nr: {self.id}'
