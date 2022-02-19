from django.db import models
from django.contrib.gis.db.models import PointField
from django_fsm import FSMField, transition
from .choices import ActivityChoices, StatusChoices


class Houmer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.phone}'


class ScheduledVisit(models.Model):
    scheduled_date_at = models.DateTimeField()
    scheduled_houmer = models.ForeignKey(Houmer, on_delete=models.CASCADE)
    activity = models.CharField(
        choices=ActivityChoices,
        max_length=20
    )
    status = FSMField(
        choices=StatusChoices,
        default=StatusChoices.SCHEDULED,
        protected=True,
        max_length=20
    )
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    def __str__(self):
        return f'{self.scheduled_date} - {self.scheduled_houmer}'

    @transition(field=status, source=StatusChoices.SCHEDULED, target=StatusChoices.IN_TRANSIT)
    def in_transit(self):
        """
        Side effects galore
        """
        pass

    @transition(field=status, source=StatusChoices.IN_TRANSIT, target=StatusChoices.IN_PROGRESS)
    def in_progress(self):
        """
        Side effects galore
        """
        pass

    @transition(field=status, source=StatusChoices.IN_PROGRESS, target=StatusChoices.COMPLETED)
    def completed(self):
        """
        Side effects galore
        """
        pass

    @transition(field=status, source='*', target=StatusChoices.CANCELLED)
    def cancelled(self):
        """
        Side effects galore
        """
        pass


class ScheduledVisitEvent(models.Model):
    scheduled_visit = models.ForeignKey(ScheduledVisit, on_delete=models.CASCADE)
    time_at = models.DateTimeField()
    position = PointField()
    current_status = models.CharField(
        choices=StatusChoices,
        default=StatusChoices.SCHEDULED,
        max_length=20
    )

    def __str__(self):
        return f'{self.event_date} - {self.event_houmer}'