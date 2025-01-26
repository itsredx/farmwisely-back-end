from django.urls import path
from . import views

urlpatterns = [
    path('<int:farm_id>/', views.AnalyticsView.as_view(), name='analytics-view'), #get analytics data using the farm id
]