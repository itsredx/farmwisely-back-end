from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django's user model
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phoneNumber = models.CharField(max_length=20, blank=True)
    measurementUnit = models.CharField(max_length=10, choices=[('metric', 'Metric'), ('imperial', 'Imperial')], default='metric')
    weatherAlerts = models.BooleanField(default=True)
    cropGrowthUpdates = models.BooleanField(default=False)
    farmTaskReminders = models.BooleanField(default=True)
    profileImage = models.ImageField(upload_to='profile_images/', null=True, blank=True)  # Store image path

    def __str__(self):
        return self.user.username

