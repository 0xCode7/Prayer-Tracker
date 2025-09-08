from django.db.models.signals import post_save
from django.dispatch import receiver
from prayers.models import PrayerLog
from .services import check_and_award_badges

@receiver(post_save, sender=PrayerLog)
def prayer_logged_award_badges(sender, instance, created, **kwargs):
    """
    Trigger badge checks after a new prayer log is created.
    """
    if created:
        check_and_award_badges(instance.user, instance)
