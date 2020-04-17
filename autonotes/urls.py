from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/vehicles/', include('autonotes.vehicles.urls')),
    path('api/notes/', include('autonotes.notes.urls')),
    path('api/tags/', include('autonotes.tags.urls')),
    path('api/users/', include('autonotes.users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

