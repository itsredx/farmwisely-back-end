from django.urls import path
from . import views

urlpatterns = [
    path('', views.FarmProfileListView.as_view(), name='farm-profile-list'), #get and post request
    path('<int:pk>/', views.FarmProfileDetailView.as_view(), name='farm-profile-detail'), #patch delete and get requests for individual farm profiles
]