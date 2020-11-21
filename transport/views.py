from django.shortcuts import render
from .forms import OrderForm
from .models import Order
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
import datetime
import requests
import smtplib

# Create your views here.

''' Google API'''
# hide api key?
API_KEY = ''
URL = "https://maps.googleapis.com/maps/api/distancematrix/json?"
RESTAURANT_LOCATION = 'łochowo'

'''values in minutes for different dishes'''
WAIT_TIME = {
    'PIZZA':30,
    'SOUP':5,
    'FRIES':25,
    'BURGER':40,
}

def index(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        ''' gets last queue position and then sets current queue position last + 1'''
        try:
            last_obj = Order.objects.last()
            last_position = last_obj.queue_positon
        except:
            last_position = 0

        form.save()
        form = OrderForm()
        current = Order.objects.last()
        current.queue_positon = last_position + 1
        

        ''' checks distance to customer location (in seconds)'''
        customer_location = current.city
        try:
                r = requests.get(URL + "origins=" + RESTAURANT_LOCATION + "&destinations=" + customer_location + "&key=" + API_KEY)
                distance_seconds = r.json()["rows"][0]["elements"][0]["duration"]["value"]
        except:
            distance_seconds = 0

        ''' sets wait time depending of what is ordered '''
        try:
            current.wait_time = last_obj.wait_time
        except:
            pass
        current.wait_time = current.wait_time + datetime.timedelta(minutes=WAIT_TIME[current.product])
        current.wait_time = current.wait_time + datetime.timedelta(seconds=distance_seconds)
        current.save()

        return HttpResponseRedirect(reverse('transport:wait-page', args = (current.id,))) 
    return render(request, 'transport/index.html', {'form': form})

def wait(request, order_id):
    is_delivered = False
    now = timezone.now()
    ''' deletes old queue and put in order remaining '''
    all_objects = Order.objects.all()
    deleted_obj = 0
    try:
        for obj in all_objects:
            obj.queue_positon = obj.queue_positon - deleted_obj 
            obj.save()
            if (obj.wait_time <= now):
                deleted_obj += 1
                obj.delete()
    except:
        pass

    try: 
        position = Order.objects.get(id=order_id).queue_positon
    except:
        # -1 means order has been already completed
        is_delivered = True
        position = -1

    ''' get wait time '''
    try:
        time = Order.objects.get(id=order_id).wait_time
    except:
        time = 0

    return render(request, 'transport/wait-page.html', context={'order_id': order_id, 'position': position, 'is_delivered': is_delivered, 'time': time})