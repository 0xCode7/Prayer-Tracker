from django.db import models
from django.contrib.auth.models import AbstractUser
from groups.models import Group

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    PRIVACY_PUBLIC = "public"
    PRIVACY_FRIENDS = "friends"
    PRIVACY_PRIVATE = "private"
    PRIVACY_CHOICES = [
        (PRIVACY_PUBLIC, "Everyone"),
        (PRIVACY_FRIENDS, "Friends Only"),
        (PRIVACY_PRIVATE, "Only Me"),
    ]
    privacy_setting = models.CharField(
        max_length=10, choices=PRIVACY_CHOICES, default=PRIVACY_FRIENDS
    )

    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, blank=True, null=True, related_name="members"
    )

    def __str__(self):
        return self.username
