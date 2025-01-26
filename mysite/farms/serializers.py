from rest_framework import serializers
from .models import FarmProfile

class FarmProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmProfile
        fields = [
            'id', 
            'farmName', 
            'farmLocation', 
            'farmSize', 
            'soilType', 
            'pHValue', 
            'currentCrop', 
            'futureCrop', 
            'irrigationSystem',
            'latitude', 
            'longitude',
            ] 
        # Added id to make it easier on the front end to know which profile to edit/delete
