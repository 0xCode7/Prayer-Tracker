from rest_framework import serializers
from .models import Group
from authentication.models import User

class GroupSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField(source='members.count', read_only=True)

    class Meta:
        model = Group
        fields = ["id", "name", "slug", "members_count", "created_at"]

class UserInGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "phone"]