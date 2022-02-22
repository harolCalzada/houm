from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from django_fsm import can_proceed
from django_filters.rest_framework import DjangoFilterBackend

from apps.houmer.exceptions import ScheduleVisitStatusException
from apps.houmer.choices import StatusChoices

from ..models import ScheduledVisit, ScheduledVisitStatistic
from .filters import ScheduledVisitsStatisticFilter
from .serializers import (
    ScheduledVisitCreateSerializer,
    ScheduledVisitStatusSerializer,
    ScheduledVisitSerializer,
    ScheduleVisitDetailSerializer,
    scheduledVisitStatisticSerializer
)


class ScheduledVisitViewSet(viewsets.ModelViewSet):
    queryset = ScheduledVisit.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ScheduledVisit.objects.all()
        return ScheduledVisit.objects.filter(houmer=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return ScheduledVisitCreateSerializer
        elif self.action in ['update', 'patch']:
            return ScheduledVisitStatusSerializer
        elif self.action == 'retrieve':
            return ScheduleVisitDetailSerializer

        return ScheduledVisitSerializer

    def perform_create(self, serializer):
        serializer.save(houmer=self.request.user, status=StatusChoices.SCHEDULED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        transition = instance.get_transition(request.data.get('new_status'))
        if not can_proceed(transition):
            raise ScheduleVisitStatusException('Invalid status')
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        transition(request.data.get('latitude'), request.data.get('longitude'))
        instance.save()
        return Response(serializer.data)


class ScheduledVisitStatisticListApiView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ScheduledVisitsStatisticFilter
    serializer_class = scheduledVisitStatisticSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ScheduledVisitStatistic.objects.all()
        return ScheduledVisitStatistic.objects.filter(schedule_visit__houmer=user.id)
