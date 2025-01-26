from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('profiles.urls')),
    path('api/farms/', include('farms.urls')), # added farms urls
    path('api/weather/', include('weather.urls')), # Add weather api
    path('api/chat/', include('chat.urls')), # added chat urls
    path('api/recommendations/', include('recommendations.urls')), #added the recommendations app
    path('api/analytics/', include('analytics.urls')), # added analytics app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)