from django.contrib import admin
from .models import PrayerLog

# Register your models here.


@admin.register(PrayerLog)
class PrayerLogAdmin(admin.ModelAdmin):
    list_display = ("user", "prayer", "date", "prayed", "created_at")
    list_filter = ("prayer", "prayed", "date")
    search_fields = ("user__username", "user__email")
    autocomplete_fields = ("user",)
