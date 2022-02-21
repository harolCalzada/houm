from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ScheduledVisitViewSet,
    ScheduledVisitStatisticListApiView,
)

router = DefaultRouter()
router.register(r"schedule-visits", ScheduledVisitViewSet, basename="schedule-visits")

urlpatterns = [
    path("", include(router.urls)),
    path("statistics/", ScheduledVisitStatisticListApiView.as_view(), name="statistics"),
]
