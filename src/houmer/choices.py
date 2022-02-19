from django.db import models
from django.utils.translation import gettext as _


class ActivityChoices(models.TextChoices):
    TOUR = 'TOUR', _('Tour')
    VISIT = 'VISIT', _('Visit')
    PHOTO = 'PHOTO', _('Photo')
    REPAIR = 'REPAIR', _('Repair')
    OTHER = 'OTHER', _('Other')


class StatusChoices(models.TextChoices):
    SCHEDULED = 'SCHEDULED', _('Scheduled')
    IN_TRANSIT = 'IN_TRANSIT', _('In transit')
    IN_PROGRESS = 'IN_PROGRESS', _('In progress')
    COMPLETED = 'COMPLETED', _('Completed')
    CANCELLED = 'CANCELLED', _('Cancelled')
