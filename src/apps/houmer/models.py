from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.conf import settings
from django_fsm import FSMField, transition
from .choices import ActivityChoices, StatusChoices
from ..propertie.models import Propertie
from .exceptions import ScheduleVisitStatusException


class Houmer(AbstractUser):
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.phone}'

    class Meta:
        verbose_name = _('Houmer')
        verbose_name_plural = _('Houmer')


class ScheduledVisit(models.Model):
    scheduled_date_at = models.DateTimeField()
    houmer = models.ForeignKey(Houmer, on_delete=models.CASCADE)
    propertie = models.ForeignKey(Propertie, on_delete=models.SET_NULL, null=True)
    activity = models.CharField(
        choices=ActivityChoices.choices,
        max_length=20
    )
    status = FSMField(
        choices=StatusChoices.choices,
        default=StatusChoices.SCHEDULED,
        max_length=20,
        protected=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'

    @transition(
        field=status,
        source=StatusChoices.SCHEDULED,
        target=StatusChoices.IN_TRANSIT
    )
    def in_transit(self, latitude, longitude):
        ScheduledVisitEvent.objects.create(
            scheduled_visit=self,
            position=Point(latitude, longitude, srid=settings.SRID),
            current_status=StatusChoices.IN_TRANSIT
        )
        ScheduledVisitStatistic.objects.create(
            schedule_visit=self
        )

    @transition(
        field=status,
        source=StatusChoices.IN_TRANSIT,
        target=StatusChoices.IN_PROGRESS
    )
    def in_progress(self, latitude, longitude):
        ScheduledVisitEvent.objects.create(
            scheduled_visit=self,
            position=Point(latitude, longitude, srid=settings.SRID),
            current_status=StatusChoices.IN_PROGRESS
        )
        velocity_km_x_h = self.scheduled_visit_statistic.calculate_velocity_km_x_h()
        self.scheduled_visit_statistic.velocity_km_x_h = velocity_km_x_h
        self.scheduled_visit_statistic.save()

    @transition(
        field=status,
        source=StatusChoices.IN_PROGRESS,
        target=StatusChoices.COMPLETED
    )
    def completed(self, latitude, longitude):
        ScheduledVisitEvent.objects.create(
            scheduled_visit=self,
            position=Point(latitude, longitude, srid=settings.SRID),
            current_status=StatusChoices.COMPLETED
        )
        stay_time_in_minutes = self.scheduled_visit_statistic.calculate_stay_time_in_minutes()
        self.scheduled_visit_statistic.stay_time_in_minutes = stay_time_in_minutes
        self.scheduled_visit_statistic.save()

    @transition(
        field=status,
        source='*',
        target=StatusChoices.CANCELLED
    )
    def cancelled(self, latitude, longitude):
        ScheduledVisitEvent.objects.create(
            scheduled_visit=self,
            position=Point(latitude, longitude, srid=settings.SRID),
            current_status=StatusChoices.CANCELLED
        )

    def get_transition(self, target_status: str):
        transitions = {
            StatusChoices.IN_TRANSIT: self.in_transit,
            StatusChoices.IN_PROGRESS: self.in_progress,
            StatusChoices.COMPLETED: self.completed,
            StatusChoices.CANCELLED: self.cancelled
        }
        if not transitions.get(target_status):
            raise ScheduleVisitStatusException('Invalid status')
        return transitions.get(target_status)

    def get_in_transit_event(self):
        return self.scheduled_visit_events.get(current_status=StatusChoices.IN_TRANSIT)

    def get_in_progress_event(self):
        return self.scheduled_visit_events.get(current_status=StatusChoices.IN_PROGRESS)

    def get_completed_event(self):
        return self.scheduled_visit_events.get(current_status=StatusChoices.COMPLETED)


class ScheduledVisitEvent(models.Model):
    scheduled_visit = models.ForeignKey(
        ScheduledVisit,
        on_delete=models.CASCADE,
        related_name='scheduled_visit_events'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    position = PointField()
    current_status = models.CharField(
        choices=StatusChoices.choices,
        default=StatusChoices.SCHEDULED,
        max_length=20
    )

    def __str__(self):
        return f'{self.created_at} - {self.scheduled_visit}'


class ScheduledVisitStatistic(models.Model):
    date = models.DateTimeField(auto_now=True)
    schedule_visit = models.OneToOneField(
        ScheduledVisit,
        related_name='scheduled_visit_statistic',
        on_delete=models.CASCADE
    )
    stay_time_in_minutes = models.BigIntegerField(null=True)
    velocity_km_x_h = models.BigIntegerField(null=True)

    class Meta:
        verbose_name = 'Scheduled Visit Report'
        verbose_name_plural = 'Scheduled Visit Reports'

    def __str__(self):
        return str(self.id)

    def calculate_velocity_km_x_h(self):
        in_transit_event = self.schedule_visit.get_in_transit_event()
        in_progress_event = self.schedule_visit.get_in_progress_event()
        distance_in_km = in_progress_event.position.distance(in_transit_event.position) * 100
        travel_time_in_hour = float((in_progress_event.created_at - in_transit_event.created_at).total_seconds() / 3600)
        return int(distance_in_km / travel_time_in_hour)

    def calculate_stay_time_in_minutes(self):
        in_progress_event = self.schedule_visit.get_in_progress_event()
        completed_event = self.schedule_visit.get_completed_event()
        return int((completed_event.created_at - in_progress_event.created_at).total_seconds() / 60)
