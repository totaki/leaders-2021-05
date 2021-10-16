from rest_framework.routers import DefaultRouter

from density.views import SmallHexViewSet, BigHexViewSet

router = DefaultRouter(trailing_slash=False)
router.register('big-hex', BigHexViewSet)
router.register('small-hex', SmallHexViewSet)

urlpatterns = [
    *router.urls
]
