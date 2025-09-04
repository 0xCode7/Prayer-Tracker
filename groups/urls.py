from django.urls import path
from .views import CreateGroupView, JoinGroupView, GroupDetailView, GroupLeaderboardView

urlpatterns = [
    path("create/", CreateGroupView.as_view(), name="group-create"),
    path("join/", JoinGroupView.as_view(), name="group-join"),
    path("me/", GroupDetailView.as_view(), name="my-group-detail"),
    path("me/leaderboard/", GroupLeaderboardView.as_view(), name="my-group-leaderboard"),
]
