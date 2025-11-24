from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("cleaning/", include("apps.cleaning_logs.urls")),
    path("billing/", include("apps.billing.urls")),
    path("equipment/", include("apps.equipment.urls")),

    # Homepage as fallback (must be last)
    path("", views.home, name="home"),
]

# Servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
