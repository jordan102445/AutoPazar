from rest_framework.routers import DefaultRouter

from .views import InquiryMessageViewSet

router = DefaultRouter()
router.register("", InquiryMessageViewSet, basename="api-inquiry")

urlpatterns = router.urls

