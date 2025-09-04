from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from groups.models import Group
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "phone", "group", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "group")
    search_fields = ("username", "email", "phone")
    ordering = ("username",)
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("phone", "group")}),
    )
