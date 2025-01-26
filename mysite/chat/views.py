from rest_framework import generics, permissions, authentication
from rest_framework.response import Response
from rest_framework import status
from .services import get_ai_response
from farms.models import FarmProfile
from weather.services import fetch_weather_data
from .models import ChatHistory, ChatMessage
from .serializers import ChatHistorySerializer

class ChatView(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, farm_id):
        user_message = request.data.get('message')
        chat_title = request.data.get('chat_title', user_message[:20])  # Default to first 20 chars if title not provided
        if not user_message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            farm = FarmProfile.objects.get(id=farm_id, user=request.user) # Get farm data
        except FarmProfile.DoesNotExist:
            return Response({'error': 'Farm profile not found'}, status=status.HTTP_404_NOT_FOUND)
        weather_data = None
        if farm.latitude is not None and farm.longitude is not None:
              weather_data = fetch_weather_data(farm.latitude, farm.longitude) #Get weather data
        # Create the system prompt
        system_prompt = f"farm location {farm.farmLocation} , "
        if weather_data:
            system_prompt += f"wether {weather_data['currentConditions']['temp']}c , {weather_data['currentConditions']['conditions']}  "
        system_prompt += "You are an AI farm adviser, provide accurate answers and recommendations, keep the responses concise, you must always provide information from the data provided, if you dont have that information just say so."
        ai_response = get_ai_response(system_prompt, user_message)
        if ai_response:
            # Retrieve or create chat history
            chat_history, created = ChatHistory.objects.get_or_create(
                  user=request.user, # add the user here
                   farm=farm,
                   title=chat_title,  # set the title
            )
            ChatMessage.objects.create(history=chat_history, sender='user', text=user_message)
            ChatMessage.objects.create(history=chat_history, sender='ai', text=ai_response)
            serializer = ChatHistorySerializer(chat_history)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Error getting ai response'}, status=status.HTTP_400_BAD_REQUEST)

class ChatHistoryListView(generics.ListAPIView):
    serializer_class = ChatHistorySerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatHistory.objects.filter(user=user)

class ChatHistoryDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ChatHistorySerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return ChatHistory.objects.filter(user=user)