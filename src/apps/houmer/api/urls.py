from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ScheduledVisitViewSet
)

router = DefaultRouter()
router.register(r"schedule-visits", ScheduledVisitViewSet, basename="schedule-visits")

urlpatterns = [
    path("", include(router.urls)),
]
