from django.contrib import admin
from .models import FarmProfile
    
@admin.register(FarmProfile)
class FarmProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'farmName', 'farmLocation', 'soilType', 'latitude', 'longitude']
    search_fields = ['user__username', 'farmName', 'farmLocation']