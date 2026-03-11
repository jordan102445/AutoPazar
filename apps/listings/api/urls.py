from rest_framework.routers import DefaultRouter

from .views import ListingViewSet, MyListingViewSet

router = DefaultRouter()
router.register("mine", MyListingViewSet, basename="api-my-listing")
router.register("", ListingViewSet, basename="api-listing")

urlpatterns = router.urls
