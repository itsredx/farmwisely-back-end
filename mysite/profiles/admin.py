from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email', 'phoneNumber', 'measurementUnit'] # this will show the user, name, email, etc, on the admin panel
    search_fields = ['user__username', 'name', 'email'] #allow you to search the profiles based on user, name and email