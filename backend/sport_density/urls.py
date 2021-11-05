from rest_framework.routers import DefaultRouter

from sport_density.views import SmallHexViewSet, HexIntersectionViewSet, BigHexViewSet, SquareColorBinsViewSet, \
    SquarePerPersonColorBinsViewSet

router = DefaultRouter(trailing_slash=False)
router.register('small-hex', SmallHexViewSet)
router.register('big-hex', BigHexViewSet)
router.register('small-hex-intersections', HexIntersectionViewSet)
router.register('color-bins-by-square', SquareColorBinsViewSet)
router.register('color-bins-by-square-per-person', SquarePerPersonColorBinsViewSet)

urlpatterns = [
    *router.urls
]
