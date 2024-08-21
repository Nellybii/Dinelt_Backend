from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from foodie_app.models import Accommodation
from foodie_app.serializer import AccommodationSerializer
import logging

logger = logging.getLogger(__name__)

class AccommodationCreateView(generics.CreateAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        # Ensure the restaurant is retrieved correctly
        restaurant = serializer.validated_data.get('restaurant')
        if not restaurant:
            raise PermissionDenied("Restaurant must be provided for accommodation creation.")
        if not (user == restaurant.owner or user in restaurant.managers.all()):
            logger.warning(f"Unauthorized creation attempt by user: {user.username} for restaurant: {restaurant.id}")
            raise PermissionDenied("You do not have permission to create accommodations for this restaurant.")
        serializer.save()
        logger.info(f"Accommodation created successfully for restaurant: {restaurant.id}")
# class AccommodationCreateView(generics.CreateAPIView):
    # queryset = Accommodation.objects.all()
    # serializer_class = AccommodationSerializer
    # permission_classes = [permissions.IsAuthenticated]
# 
    # def perform_create(self, serializer):
        # user = self.request.user
        # restaurant = serializer.validated_data.get('restaurant')
        # if not (user == restaurant.owner or user in restaurant.managers.all()):
            # logger.warning(f"Unauthorized create attempt by user: {user.username} for restaurant: {restaurant.id}")
            # raise PermissionDenied("You do not have permission to create accommodation for this restaurant.")
        # serializer.save()
        # logger.info(f"Accommodation created successfully for restaurant: {restaurant.id}")

class AccommodationListView(generics.ListAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    permission_classes = [permissions.AllowAny]

class AccommodationDetailView(generics.RetrieveAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    permission_classes = [permissions.AllowAny]

class AccommodationUpdateView(generics.UpdateAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        user = self.request.user
        accommodation = self.get_object()
        if not (user == accommodation.restaurant.owner or user in accommodation.restaurant.managers.all()):
            logger.warning(f"Unauthorized update attempt by user: {user.username} on accommodation: {accommodation.id}")
            raise PermissionDenied("You do not have permission to update this accommodation.")
        serializer.save()
        logger.info(f"Accommodation updated successfully: {accommodation.id}")

class AccommodationDeleteView(generics.DestroyAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        user = self.request.user
        if not (user == instance.restaurant.owner or user in instance.restaurant.managers.all()):
            logger.warning(f"Unauthorized delete attempt by user: {user.username} on accommodation: {instance.id}")
            raise PermissionDenied("You do not have permission to delete this accommodation.")
        instance.delete()
        logger.info(f"Accommodation deleted successfully: {instance.id}")
