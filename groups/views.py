from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from prayers.models import PrayerLog
from .models import Group
from .serializers import GroupSerializer, UserInGroupSerializer
from django.utils.timezone import now
from django.db.models import Count, Q


# Create your views here.
class CreateGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get("name")

        if not name:
            return Response({"error": "Group name is required"}, status=status.HTTP_400_BAD_REQUEST)

        group = Group.objects.create(name=name)
        request.user.group = group
        request.user.save()

        return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)


class JoinGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        slug = request.data.get('slug')
        if not slug:
            return Response({"error": "Group slug is required"}, status=status.HTTP_400_BAD_REQUEST)
        group = get_object_or_404(Group, slug=slug)

        if request.user.group:
            return Response({"error": "You are already in a group"}, status=status.HTTP_400_BAD_REQUEST)
        request.user.group = group

        request.user.save()
        return Response({"message": f"Joined {group.name} successfully"})


class GroupDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.group:
            return Response({"message": "You are not in a group"}, status=404)

        group = user.group
        serializer = GroupSerializer(group)
        members = UserInGroupSerializer(group.members.all(), many=True)

        return Response({
            "group": serializer.data,
            "members": members.data
        })


class GroupLeaderboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug=None):
        # لو بslug أو group بتاع اليوزر
        if slug:
            group = get_object_or_404(Group, slug=slug)
        else:
            group = request.user.group
            if not group:
                return Response({"message": "You are not in a group"}, status=404)

        today = now().today()
        start_week = today - timedelta(days=today.weekday())
        start_month = today.replace(day=1)

        leaderboard = []
        for member in group.members.all():
            week_count = PrayerLog.objects.filter(
                user=member, prayed=True, date__gte=start_week, date__lte=today
            ).count()
            month_count = PrayerLog.objects.filter(
                user=member, prayed=True, date__gte=start_month, date__lte=today
            ).count()

            leaderboard.append({
                "username": member.username,
                "week_count": week_count,
                "month_count": month_count,
            })

        # الترتيب: الأول بالأسبوع وبعدين بالشهر
        leaderboard = sorted(
            leaderboard,
            key=lambda x: (-x["week_count"], -x["month_count"])
        )

        return Response({
            "group": group.name,
            "leaderboard": leaderboard
        })
