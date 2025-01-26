from django.urls import path
from . import views

urlpatterns = [
    path('<int:farm_id>/', views.RecommendationView.as_view(), name='recommendation-view'), #get recommendations using a farm profile id
]