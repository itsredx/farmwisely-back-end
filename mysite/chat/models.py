from django.db import models
from django.contrib.auth.models import User
from farms.models import FarmProfile

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_histories')
    farm = models.ForeignKey(FarmProfile, on_delete=models.CASCADE, related_name='chat_histories')
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
       return f"Chat History: {self.title} User: {self.user.username}"

class ChatMessage(models.Model):
     history = models.ForeignKey(ChatHistory, on_delete=models.CASCADE, related_name='messages')
     sender = models.CharField(max_length=50)
     text = models.TextField()
     timestamp = models.DateTimeField(auto_now_add=True)

     def __str__(self):
        return f"Message from {self.sender}: {self.text}"