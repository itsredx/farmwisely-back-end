from rest_framework import generics, permissions, authentication
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.contrib.auth import authenticate


class RegisterView(generics.CreateAPIView):
   
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
   
   
    def post(self, request):
      try:
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        user = User.objects.create_user(username=username, password=password, email=email)
        token = Token.objects.create(user=user)
        UserProfile.objects.create(user=user) #create an empty profile
        return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_201_CREATED)
      except Exception as e:
        return Response({'error': 'Error while trying to create a new user', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.CreateAPIView):
     
     permission_classes = (permissions.AllowAny,)
     
     
     def post(self, request):
          username = request.data.get('username')
          password = request.data.get('password')
          user = authenticate(username=username, password=password)
          if user:
              token, _ = Token.objects.get_or_create(user=user)
              return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
          else:
              return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(generics.RetrieveUpdateAPIView):
    
    serializer_class = UserProfileSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get_object(self):
        user = self.request.user
        return user.userprofile
