from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/prayers/', include('prayers.urls')),
    path('api/groups/', include('groups.urls')),
]
