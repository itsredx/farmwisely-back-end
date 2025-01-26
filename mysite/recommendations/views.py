from rest_framework import generics, permissions, authentication
from rest_framework.response import Response
from rest_framework import status
from .services import get_crop_recommendations
from farms.models import FarmProfile
from weather.services import fetch_weather_data

class RecommendationView(generics.GenericAPIView):
     authentication_classes = [authentication.TokenAuthentication]
     permission_classes = [permissions.IsAuthenticated]
     def get(self, request, farm_id):
          try:
             farm = FarmProfile.objects.get(id=farm_id, user=request.user) # Get farm data
          except FarmProfile.DoesNotExist:
              return Response({'error': 'Farm profile not found'}, status=status.HTTP_404_NOT_FOUND)
          weather_data = None
          if farm.latitude is not None and farm.longitude is not None:
              weather_data = fetch_weather_data(farm.latitude, farm.longitude) #Get weather data
          farm_data = {
              'soilType': farm.soilType,
              'pHValue': farm.pHValue,
              'farmSize': farm.farmSize,
           }
          user_notes = request.query_params.get('notes')  # Get user notes from query parameters
          recommendations = get_crop_recommendations(farm_data, weather_data, user_notes) #pass the weather data
          if recommendations:
              return Response(recommendations, status=status.HTTP_200_OK)
          else:
             return Response({'error': 'Error getting recommendations'}, status=status.HTTP_400_BAD_REQUEST)