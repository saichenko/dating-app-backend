from rest_framework.routers import DefaultRouter

from .viewsets import PrecedenceViewSet, UsersPrecedencyViewSet

router = DefaultRouter()
router.register(
    r"precedency",
    PrecedenceViewSet,
    basename="precedency"
)
router.register(
    r"user-precedency",
    UsersPrecedencyViewSet,
    basename="user-precedency"
)
urlpatterns = router.urls
