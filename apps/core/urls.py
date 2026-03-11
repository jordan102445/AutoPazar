from django.urls import path

from .views import ContactPageView, HomePageView, healthcheck

app_name = "core"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("kontakt/", ContactPageView.as_view(), name="contact"),
    path("health/", healthcheck, name="healthcheck"),
]

