from rest_framework.routers import DefaultRouter

from .views import ListingReportViewSet

router = DefaultRouter()
router.register("", ListingReportViewSet, basename="api-report")

urlpatterns = router.urls

