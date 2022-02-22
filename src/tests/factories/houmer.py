from datetime import datetime
from django.contrib.gis.geos import Point
from django.conf import settings
from apps.houmer.models import Houmer, ScheduledVisit
from apps.propertie.models import Propertie
from apps.houmer.choices import ActivityChoices, StatusChoices


def houmer_factory(
    first_name: str,
    last_name: str,
    username: str,
    password: str,
    phone: str = '+5199999999'
) -> Houmer:
    return Houmer.objects.create(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        username=username,
        password=password
    )


def scheduled_visit_factory(
    houmer: Houmer,
    scheduled_date_at: datetime,
    propertie: Propertie,
    activity: str = ActivityChoices.TOUR,
    status: str = StatusChoices.SCHEDULED
) -> ScheduledVisit:
    return ScheduledVisit.objects.create(
        houmer=houmer,
        scheduled_date_at=scheduled_date_at,
        propertie=propertie,
        activity=activity,
        status=status
    )
