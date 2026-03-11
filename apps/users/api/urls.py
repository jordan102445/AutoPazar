from django.urls import path

from .views import CurrentProfileView, PublicSellerProfileView

urlpatterns = [
    path("me/", CurrentProfileView.as_view(), name="api-profile-me"),
    path("sellers/<int:pk>/", PublicSellerProfileView.as_view(), name="api-public-seller"),
]

