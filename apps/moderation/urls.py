from django.urls import path

from .views import ListingReportCreateView

app_name = "moderation"

urlpatterns = [
    path("<slug:slug>/prijavi/", ListingReportCreateView.as_view(), name="report"),
]

