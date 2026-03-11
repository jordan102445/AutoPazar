from django.urls import path

from .views import InboxListView, InquiryCreateView, InquiryStatusUpdateView

app_name = "messaging"

urlpatterns = [
    path("inbox/", InboxListView.as_view(), name="inbox"),
    path("<slug:slug>/new/", InquiryCreateView.as_view(), name="create"),
    path("inbox/<int:pk>/status/", InquiryStatusUpdateView.as_view(), name="status"),
]

