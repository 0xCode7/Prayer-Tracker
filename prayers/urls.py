from django.urls import path
from .views import (PrayerLogView,TodayPrayersView, WeekPrayersView,MonthPrayersView
    )

urlpatterns = [
    path('log/', PrayerLogView.as_view(), name='prayer-log'),
    path('day/', TodayPrayersView.as_view(), name='prayer-day'),
    path('week/', WeekPrayersView.as_view(), name='prayer-week'),
    path('month/', MonthPrayersView.as_view(), name='prayer-month'),
]
