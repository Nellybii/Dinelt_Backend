from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from foodie_app.models import Reservation
from foodie_app.serializer import ReservationSerializer
from rest_framework.exceptions import PermissionDenied

class ReservationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return only the reservations for the currently authenticated user.
        """
        user = self.request.user
        return Reservation.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Save the user as the author of the reservation.
        """
        serializer.save(user=self.request.user)

class ReservationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return only the reservations for the currently authenticated user.
        """
        user = self.request.user
        return Reservation.objects.filter(user=user)

    def get_object(self):
        """
        Return the object for the current user and the specified reservation ID.
        """
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to access this reservation.")
        return obj
