from django.utils.timezone import localdate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import date, timedelta
from django.utils.timezone import now
from prayers.serializers import PrayerLogSerializer
from .models import PrayerLog


# Create your views here.
class PrayerLogView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PrayerLogSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            prayer_log = serializer.save()
            return Response(PrayerLogSerializer(prayer_log).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodayPrayersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()
        logs = PrayerLog.objects.filter(user=request.user, date=today)
        serializer = PrayerLogSerializer(logs, many=True)

        return Response({
            "date": today,
            "prayers": serializer.data
        })

class WeekPrayersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)

        logs = PrayerLog.objects.filter(user=request.user, date__range=[start_week, end_week])
        serializer = PrayerLogSerializer(logs, many=True)

        return Response({
            "start_week": start_week,
            "end_week": end_week,
            "count": logs.count(),
            "prayers": serializer.data
        })


class MonthPrayersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = localdate()
        start_month = today.replace(day=1)

        logs = PrayerLog.objects.filter(user=request.user, date__gte=start_month, date__lte=today)

        serializer = PrayerLogSerializer(logs, many=True)

        return Response({
            "month": today.strftime("%B %Y"),
            "count": logs.count(),
            "prayers": serializer.data
        })
