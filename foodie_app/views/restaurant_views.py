from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from foodie_app.models import Restaurant, Manager
from foodie_app.serializer import RestaurantSerializer, ManagerSerializer
import logging

logger = logging.getLogger(__name__)

class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.AllowAny]

class RestaurantDetailView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.AllowAny]

class RestaurantCreateView(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        
        logger.info(f"Creating restaurant with user: {user.username}, is_business_owner: {user.is_business_owner}")

        if not user.is_business_owner:
            raise PermissionDenied("You must be a business owner to create a restaurant.")
        
        serializer.save(owner=user)

class RestaurantUpdateView(generics.UpdateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        restaurant = self.get_object()
        if request.user != restaurant.owner and not Manager.objects.filter(user=request.user, restaurant=restaurant).exists():
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return self.update(request, *args, **kwargs)

class RestaurantDeleteView(generics.DestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        restaurant = self.get_object()
        if request.user != restaurant.owner and not Manager.objects.filter(user=request.user, restaurant=restaurant).exists():
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return self.destroy(request, *args, **kwargs)

class ManagerCreateView(generics.CreateAPIView):
    serializer_class = ManagerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        restaurant = serializer.validated_data['restaurant']
        if self.request.user != restaurant.owner:
            raise PermissionDenied("You can only add managers to restaurants you own.")
        serializer.save()
