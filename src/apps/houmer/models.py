from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db.models import PointField
from django_fsm import FSMField, transition
from .choices import ActivityChoices, StatusChoices
from ..propertie.models import Propertie


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
        max_length=20
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.scheduled_date_at} - {self.houmer}'

    @transition(
        field=status,
        source=StatusChoices.SCHEDULED,
        target=StatusChoices.IN_TRANSIT
    )
    def in_transit(self):
        """
        Side effects galore
        """
        pass

    @transition(
        field=status,
        source=StatusChoices.IN_TRANSIT,
        target=StatusChoices.IN_PROGRESS
    )
    def in_progress(self):
        pass

    @transition(
        field=status,
        source=StatusChoices.IN_PROGRESS,
        target=StatusChoices.COMPLETED
    )
    def completed(self):
        pass

    @transition(
        field=status,
        source='*',
        target=StatusChoices.CANCELLED
    )
    def cancelled(self):
        pass


class ScheduledVisitEvent(models.Model):
    scheduled_visit = models.ForeignKey(ScheduledVisit, on_delete=models.CASCADE)
    time_at = models.DateTimeField()
    position = PointField()
    current_status = models.CharField(
        choices=StatusChoices.choices,
        default=StatusChoices.SCHEDULED,
        max_length=20
    )

    def __str__(self):
        return f'{self.event_date} - {self.event_houmer}'