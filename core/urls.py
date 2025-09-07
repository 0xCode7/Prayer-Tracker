from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/prayers/', include('prayers.urls')),
    path('api/groups/', include('groups.urls')),
    # YOUR PATTERNS
    path('download/', SpectacularAPIView.as_view(), name='schema-yaml'),
    # Optional UI:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='schema-ui'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
