from rest_framework import generics, permissions
from foodie_app.models import OrderItem, Order
from foodie_app.serializer import OrderItemSerializer, OrderSerializer


class OrderItemCreateView(generics.ListCreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically link the order item to the authenticated user
        serializer.save(user=self.request.user)

class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter to only include order items for the authenticated user
        return OrderItem.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        # Update the order item while ensuring it's linked to the authenticated user
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # Ensure the order item belongs to the authenticated user before deletion
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise permissions.PermissionDenied("You do not have permission to delete this order item.")
    

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise permissions.PermissionDenied("You do not have permission to delete this order.")
