from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("auth/token/", obtain_auth_token, name="api-token"),
    path("users/", include("apps.users.api.urls")),
    path("listings/", include("apps.listings.api.urls")),
    path("favorites/", include("apps.favorites.api.urls")),
    path("messages/", include("apps.messaging.api.urls")),
    path("reports/", include("apps.moderation.api.urls")),
]

