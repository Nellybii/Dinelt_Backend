from foodie_app.models import User, Profile
from foodie_app.serializer import MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

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
@permission_classes([IsAuthenticated])
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
    print(permission_classes)

    def get_object(self):
        user = self.request.user
        print(user)
        if not user.is_authenticated:
            logger.error("Unauthorized access attempt")
            raise PermissionDenied("User not authenticated")
        try:
            profile = Profile.objects.get(user=user)
            logger.info(f"Profile retrieved for user {user.username}")
        except Profile.DoesNotExist:
            logger.error(f"Profile not found for user {user.username}")
            raise NotFound("Profile not found")
        return profile
    
class ProfileUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class =ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
