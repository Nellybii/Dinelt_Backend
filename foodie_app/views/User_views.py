from django.shortcuts import render, get_object_or_404
from foodie_app.models import User, Profile
from foodie_app.serializer import MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions
from django.views.generic import DetailView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/',
        '/api/profile/',
        '/api/profile/update/'
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulations {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = "Hello buddy"
        data = f'Congratulations, your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)

class ProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if not user.is_authenticated:
            logger.error("Unauthorized access attempt")
            raise PermissionDenied("User not authenticated")
        
        try:
            profile = Profile.objects.get(user=user)
            logger.info(f"Profile retrieved for user {user.username}")
            return profile
        except Profile.DoesNotExist:
            logger.error(f"Profile not found for user {user.username}")
            raise NotFound("Profile not found")
class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'