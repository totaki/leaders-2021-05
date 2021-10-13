from rest_framework.routers import DefaultRouter

from facilities.views import (
    DepartmentsViewSet, FacilitiesViewSet, SportTypesViewSet, SportsAreaTypesViewSet,
    SportsAreasViewSet
)

router = DefaultRouter(trailing_slash=False)
router.register('departments', DepartmentsViewSet)
router.register('facilities', FacilitiesViewSet)
router.register('sport-types', SportTypesViewSet)
router.register('sport-areas', SportsAreasViewSet)
router.register('sport-area-types', SportsAreaTypesViewSet)

urlpatterns = [
    *router.urls
]
