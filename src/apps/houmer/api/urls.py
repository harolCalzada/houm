from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ScheduledVisitViewSet,
    ScheduledVisitStatisticListApiView,
)

router = DefaultRouter()
router.register(r"scheduled-visit", ScheduledVisitViewSet, basename="schedule-visit")

urlpatterns = [
    path("houmer/", include(router.urls)),
    path("houmer/statistic/", ScheduledVisitStatisticListApiView.as_view(), name="statistic"),
]
