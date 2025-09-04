from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Badge(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    icon = models.ImageField(upload_to="badges/", blank=True, null=True)

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="badges")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "badge")

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"
