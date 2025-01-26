from rest_framework import generics, permissions, authentication
from rest_framework.response import Response
from rest_framework import status
from .services import fetch_weather_data
class WeatherView(generics.GenericAPIView):
     authentication_classes = [authentication.TokenAuthentication]
     permission_classes = [permissions.IsAuthenticated]

     def get(self, request, latitude, longitude):
        weather_data = fetch_weather_data(latitude, longitude)

        if weather_data:
           return Response(weather_data, status=status.HTTP_200_OK)
        else:
           return Response(
            {'error': 'Error getting weather data'}, 
            status=status.HTTP_400_BAD_REQUEST,
            )