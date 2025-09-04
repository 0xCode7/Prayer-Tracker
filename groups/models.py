# groups/models.py
from django.db import models
from django.conf import settings
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL

class Group(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            base = self.slug
            i = 2
            while Group.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base}-{i}"
                i += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
