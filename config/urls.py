from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("korisnici/", include("apps.users.urls")),
    path("oglasi/", include("apps.listings.urls")),
    path("omileni/", include("apps.favorites.urls")),
    path("poraki/", include("apps.messaging.urls")),
    path("moderacija/", include("apps.moderation.urls")),
    path("api/", include("config.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "apps.core.views.handler404"
handler500 = "apps.core.views.handler500"

