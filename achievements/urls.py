from django.urls import path
from .views import BadgeListView, UserBadgeListView

urlpatterns = [
    path("", BadgeListView.as_view(), name="badge-list"),
    path("user/<int:user_id>", UserBadgeListView.as_view(), name="user-badges"),
]
