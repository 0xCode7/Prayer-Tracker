from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your models here.
class PrayerLog(models.Model):
    PRAYER_FAJR = "fajr"
    PRAYER_DHUHR = "dhuhr"
    PRAYER_ASR = "asr"
    PRAYER_MAGHRIB = "maghrib"
    PRAYER_ISHA = "isha"

    PRAYER_CHOICES = [
        (PRAYER_FAJR, "Fajr"),
        (PRAYER_DHUHR, "Dhuhr"),
        (PRAYER_ASR, "Asr"),
        (PRAYER_MAGHRIB, "Maghrib"),
        (PRAYER_ISHA, "Isha"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prayer_log')
    prayer = models.CharField(max_length=10, choices=PRAYER_CHOICES)
    date = models.DateField()
    prayed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "prayer", "date"],
                name="unique_user_prayer_date"
            ),
        ]

        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["prayer", "date"])
        ]

        ordering = ["-date", "-created_at"]
