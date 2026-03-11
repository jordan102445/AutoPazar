from rest_framework.routers import DefaultRouter

from .views import FavoriteViewSet

router = DefaultRouter()
router.register("", FavoriteViewSet, basename="api-favorite")

urlpatterns = router.urls

