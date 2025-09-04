from django.contrib import admin
from .models import Group

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "member_count", "created_at")
    prepopulated_fields = {"slug": ("name",)}  # auto-generate slug from name
    search_fields = ("name",)

    def member_count(self, obj):
        return obj.members.count()  # uses related_name from User.group
    member_count.short_description = "Number of members"
