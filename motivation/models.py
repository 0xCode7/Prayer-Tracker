from django.db import models

# Create your models here.
from django.db import models

class Motivation(models.Model):
    text = models.TextField()
    source = models.CharField(max_length=255, blank=True, null=True)  # e.g. Qur'an, Hadith, Quote

    def __str__(self):
        return f"{self.text[:50]}..."  # first 50 chars
