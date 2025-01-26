from rest_framework import serializers
from .models import ChatHistory, ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['sender', 'text', 'timestamp']

class ChatHistorySerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatHistory
        fields = [
            'id', 
            'title', 
            'messages', 
            'created_at',
            ] 
        #add the id to make it easier on the front end to delete/get the chat histories.