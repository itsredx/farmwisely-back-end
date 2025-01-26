from django.contrib import admin
from .models import ChatHistory, ChatMessage

class ChatMessageInline(admin.TabularInline):
     model = ChatMessage
     extra = 0 #remove extra blank fields

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
     list_display = ['user', 'farm', 'title', 'created_at']
     search_fields = ['user__username', 'farm__farmName', 'title']
     inlines = [ChatMessageInline]  # Add the ChatMessageInline here


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
     list_display = ['history', 'sender', 'text', 'timestamp']
     search_fields = ['history__title', 'sender', 'text']