from rest_framework import generics, permissions, authentication
from .models import FarmProfile
from .serializers import FarmProfileSerializer


class FarmProfileListView(generics.ListCreateAPIView): # get all the farms or create new one
    serializer_class = FarmProfileSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
         user = self.request.user
         return FarmProfile.objects.filter(user=user)

    def perform_create(self, serializer): # add the user automatically when creating new farm
        serializer.save(user=self.request.user)

class FarmProfileDetailView(generics.RetrieveUpdateDestroyAPIView): # get a single farm or delete one
    serializer_class = FarmProfileSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FarmProfile.objects.filter(user=user)