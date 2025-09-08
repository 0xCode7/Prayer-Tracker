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
        start_week = today - timedelta(days=today.weekday())  # Monday
        end_week = start_week + timedelta(days=6)

        # كل صلوات الأسبوع
        logs = PrayerLog.objects.filter(
            user=request.user,
            date__range=[start_week, end_week]
        ).order_by("date")

        # ترتيب الصلوات
        prayer_order = ["fajr", "dhuhr", "asr", "maghrib", "isha"]

        # تجهيز response
        prayers_data = []
        for i in range(7):
            day_date = start_week + timedelta(days=i)
            day_logs = logs.filter(date=day_date)

            prayed_list = []
            for prayer in prayer_order:
                log = next((l for l in day_logs if l.prayer == prayer), None)
                prayed_list.append(log.prayed if log else False)

            prayers_data.append({
                "day": day_date.strftime("%a"),  # Mon, Tue, ...
                "date": str(day_date),
                "prayed": prayed_list
            })

        return Response({
            "start_week": start_week,
            "end_week": end_week,
            "total_prayed": logs.filter(prayed=True).count(),
            "prayers": prayers_data
        })


class MonthPrayersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = localdate()
        start_month = today.replace(day=1)

        # حساب آخر يوم في الشهر
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
        end_month = next_month - timedelta(days=1)

        # جميع السجلات للشهر
        logs = PrayerLog.objects.filter(
            user=request.user,
            date__range=[start_month, end_month]
        ).order_by("date")

        prayer_order = ["fajr", "dhuhr", "asr", "maghrib", "isha"]

        prayers_data = []
        current_day = start_month
        while current_day <= end_month:
            day_logs = logs.filter(date=current_day)

            prayed_list = []
            for prayer in prayer_order:
                log = next((l for l in day_logs if l.prayer == prayer), None)
                prayed_list.append(log.prayed if log else False)

            prayers_data.append({
                "date": str(current_day),
                "prayed": prayed_list
            })

            current_day += timedelta(days=1)

        return Response({
            "start_month": str(start_month),
            "end_month": str(end_month),
            "total_prayed": logs.filter(prayed=True).count(),
            "prayers": prayers_data
        })
