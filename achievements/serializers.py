from rest_framework import serializers
from .models import Badge, UserBadge

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ["id", "name", "description", "icon"]



class UserBadgeSerializer(serializers.ModelSerializer):
    badge_id = serializers.IntegerField(source="badge.id", read_only=True)
    name = serializers.CharField(source="badge.name", read_only=True)
    description = serializers.CharField(source="badge.description", read_only=True)
    icon = serializers.ImageField(source="badge.icon", read_only=True)

    class Meta:
        model = UserBadge
        fields = ["badge_id", "name", "description", "icon", "awarded_at"]