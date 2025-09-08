from datetime import timedelta, date
from django.utils import timezone
from .models import Badge, UserBadge
from prayers.models import PrayerLog


def award_badge(user, badge_name, description):
    """
        Assign a badge to the user if not already awarded.
        Creates the badge if it doesn't exist.
    """

    badge, created = Badge.objects.get_or_create(
        name=badge_name,
        defaults={'description': description}
    )

    UserBadge.objects.get_or_create(user=user, badge=badge)


def compute_fajr_streak_days(user):
    """
       Count how many consecutive days the user has prayed Fajr.
    """

    today = date.today()
    streak = 0
    day = today

    while PrayerLog.objects.filter(user=user, prayer='fajr', date=day).exists():
        streak +=1
        day -= timedelta(days=1)

    return streak


def check_full_week_all_prayers(user):
    """
        Check if the user has prayed all 5 daily prayers
        for 7 consecutive days.
    """

    today = date.today()
    last_week = [today-timedelta(days=i) for i in range(7)]
    for d in last_week:
        prayers = PrayerLog.objects.filter(user=user, date=d).values_list("prayer", flat=True)
        if len(set(prayers)) < 5:
            return False
    return True


def check_and_award_badges(user, prayer_log):
    """
       Main logic to evaluate user activity and award badges.
       Called automatically when a new prayer is logged.
    """
    # 1. First prayer ever logged
    if not PrayerLog.objects.filter(user=user).exclude(id=prayer_log.id).exists():
        award_badge(user, "First Prayer Logged", "You logged your first prayer!")

    # 2. 7-day Fajr streak
    if compute_fajr_streak_days(user) >= 7:
        award_badge(user, "7-day Fajr Streak", "You prayed Fajr 7 days in a row!")

    # 3. Full week of all 5 prayers
    if check_full_week_all_prayers(user):
        award_badge(user, "Full Week Prayers", "You prayed all 5 prayers every day for a week!")
