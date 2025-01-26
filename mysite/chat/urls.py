from django.urls import path
from . import views

urlpatterns = [
     path('<int:farm_id>/', views.ChatView.as_view(), name='chat-view'),
     path('', views.ChatHistoryListView.as_view(), name='chat-history-list'), #get all the history objects
     path('<int:pk>/', views.ChatHistoryDetailView.as_view(), name='chat-history-detail'),  #get and delete single history object
]