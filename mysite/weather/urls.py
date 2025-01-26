from django.urls import path
from . import views

urlpatterns = [
    path('<str:latitude>/<str:longitude>/', views.WeatherView.as_view(), name='weather-view'), #get weather data using latitude and longitude
]