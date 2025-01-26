from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    
    profileImage = serializers.ImageField() # we add this so we can actually get images
    
    
    class Meta:
        model = UserProfile
        fields = [
            'name', 
            'email', 
            'phoneNumber', 
            'measurementUnit', 
            'weatherAlerts', 
            'cropGrowthUpdates', 
            'farmTaskReminders', 
            'profileImage',
            ]

