from rest_framework import generics
from rest_framework.response import Response

from .models import Badge, UserBadge
from .serializers import BadgeSerializer, UserBadgeSerializer

class BadgeListView(generics.ListAPIView):
    """GET /api/badges/ → List all available badges"""
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

class UserBadgeListView(generics.ListAPIView):
    """GET /api/badges/user/<id>/ → List badges earned by a user"""
    serializer_class = UserBadgeSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return UserBadge.objects.filter(user_id=user_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "badges": serializer.data
        })