from rest_framework import generics, permissions

from ..models import UserProfile
from .serializers import SellerProfileSerializer, UserProfileSerializer


class CurrentProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class PublicSellerProfileView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.select_related("user", "city")
    serializer_class = SellerProfileSerializer
    permission_classes = [permissions.AllowAny]

