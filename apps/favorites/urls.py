from django.urls import path

from .views import FavoriteListView, FavoriteToggleView

app_name = "favorites"

urlpatterns = [
    path("", FavoriteListView.as_view(), name="list"),
    path("<slug:slug>/toggle/", FavoriteToggleView.as_view(), name="toggle"),
]

