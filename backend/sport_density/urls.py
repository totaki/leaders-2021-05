from rest_framework.routers import DefaultRouter

from sport_density.views import SmallHexViewSet, HexIntersectionViewSet, BigHexViewSet

router = DefaultRouter(trailing_slash=False)
router.register('small-hex', SmallHexViewSet)
router.register('big-hex', BigHexViewSet)
router.register('small-hex-intersections', HexIntersectionViewSet)

urlpatterns = [
    *router.urls
]
