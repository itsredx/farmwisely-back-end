from rest_framework import generics, permissions, authentication
from rest_framework.response import Response
from rest_framework import status
from .services import get_farm_analytics
from farms.models import FarmProfile
from weather.services import fetch_weather_data

class AnalyticsView(generics.GenericAPIView):
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
               'currentCrop': farm.currentCrop,
           }
          user_notes = request.query_params.get('notes')  # Get user notes from query parameters
          analytics_data = get_farm_analytics(farm_data, weather_data, user_notes)
          if analytics_data:
            return Response(analytics_data, status=status.HTTP_200_OK)
          else:
            return Response({'error': 'Error getting farm analytics'}, status=status.HTTP_400_BAD_REQUEST)