from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from foodie_app.models import Food
from foodie_app.serializer import FoodSerializer
import logging

logger = logging.getLogger(__name__)

class FoodCreateView(generics.CreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_update(self, serializer):
        user = self.request.user
        food = self.get_object()
        if not (user == food.restaurant.owner or user in food.restaurant.managers.all()):
            raise PermissionDenied("You do not have permission to update this food item.")
        serializer.save()

class FoodListView(generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.AllowAny]

class FoodDetailView(generics.RetrieveAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.AllowAny]
class FoodUpdateView(generics.UpdateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        user = self.request.user
        food = self.get_object()
        if not (user == food.restaurant.owner or user in food.restaurant.managers.all()):
            logger.warning(f"Unauthorized update attempt by user: {user.username} on food item: {food.id}")
            raise PermissionDenied("You do not have permission to update this food item.")
        serializer.save()
        logger.info(f"Food item updated successfully: {food.id}")

# class FoodUpdateView(generics.UpdateAPIView):
    # queryset = Food.objects.all()
    # serializer_class = FoodSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def put(self, request, *args, **kwargs):
        # user = self.request.user
        # food = self.get_object()
        # if request.user != food.restaurant.owner and request.user != food.restaurant.manager:
            # logger.warning(f"Unauthorized update attempt by user: {user.username} on food item: {food.id}")
            # raise PermissionDenied("You do not have permission to update this food item.")
        # return self.update(request, *args, **kwargs)
        # if not (user == food.restaurant.owner or user in food.restaurant.managers.all()):
            # logger.warning(f"Unauthorized update attempt by user: {user.username} on food item: {food.id}")
            # raise PermissionDenied("You do not have permission to update this food item.")
        # serializer.save()
        # logger.info(f"Food item updated successfully: {food.id}")

class FoodDeleteView(generics.DestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        user = self.request.user
        if not (user == instance.restaurant.owner or user in instance.restaurant.managers.all()):
            logger.warning(f"Unauthorized delete attempt by user: {user.username} on food item: {instance.id}")
            raise PermissionDenied("You do not have permission to delete this food item.")
        instance.delete()
        logger.info(f"Food item deleted successfully: {instance.id}")