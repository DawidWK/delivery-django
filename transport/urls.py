from django.urls import path, include
from . import views

app_name = "transport"
urlpatterns = [
    path('', views.index, name="index"),
    path('<int:order_id>/wait/', views.wait, name="wait-page")
]