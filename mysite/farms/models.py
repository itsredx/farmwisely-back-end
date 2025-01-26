from django.db import models
from django.contrib.auth.models import User

class FarmProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farm_profiles') # link to django's user
    farmName = models.CharField(max_length=255, blank=True)
    farmLocation = models.CharField(max_length=255, blank=True)
    farmSize = models.CharField(max_length=50, blank=True)  # Or use a numeric field if needed
    soilType = models.CharField(max_length=20, choices=[('Sandy', 'Sandy'), ('Clay', 'Clay'), ('Loamy', 'Loamy')], default='Sandy')
    pHValue = models.FloatField(default=7.0)
    currentCrop = models.CharField(max_length=20, choices=[('Maize', 'Maize'), ('Rice', 'Rice'), ('Beans', 'Beans')], default='Maize')
    futureCrop = models.CharField(max_length=20, choices=[('Maize', 'Maize'), ('Rice', 'Rice'), ('Beans', 'Beans')], default='Beans')
    irrigationSystem = models.CharField(max_length=20, choices=[('Manual', 'Manual'), ('Drip Irrigation', 'Drip Irrigation'), ('Sprinkler System', 'Sprinkler System'), ('Rain-fed', 'Rain-fed')], default='Manual')
    latitude = models.FloatField(null=True, blank=True) # add latitude to the model
    longitude = models.FloatField(null=True, blank=True) # add longitude to the model

    def __str__(self):
        return f"{self.farmName} - {self.user.username}" # Or return self.farmName if you prefer