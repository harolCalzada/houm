import pytest
from datetime import datetime
from apps.houmer.models import (
    Houmer,
    ScheduledVisit,
)
from apps.houmer.choices import StatusChoices, ActivityChoices
from ..factories.houmer import houmer_factory, scheduled_visit_factory


@pytest.fixture
def houmer_a(db) -> Houmer:
    return houmer_factory(
        first_name='houmer_a',
        last_name='houmer_a',
        username='houmer_a',
        password='houmer_a',
        phone='+5199999999',
    )


@pytest.fixture
def houmer_b(db) -> Houmer:
    return houmer_factory(
        first_name='houmer_b',
        last_name='houmer_b',
        username='houmer_b',
        password='houmer_b',
        phone='+5199999999',
    )


@pytest.fixture
def scheduled_visit_to_property_a(db, propertie_a, houmer_a) -> ScheduledVisit:
    return scheduled_visit_factory(
        houmer=houmer_a,
        scheduled_date_at=datetime(2020, 1, 1, 0, 0, 0),
        propertie=propertie_a,
        activity=ActivityChoices.TOUR,
        status=StatusChoices.SCHEDULED,
    )


@pytest.fixture
def scheduled_visit_to_property_b(db, propertie_b, houmer_b) -> ScheduledVisit:
    return scheduled_visit_factory(
        houmer=houmer_b,
        scheduled_date_at=datetime(2020, 1, 1, 0, 0, 0),
        propertie=propertie_b,
        activity=ScheduledVisit.ActivityChoices.PHOTO,
        status=ScheduledVisit.StatusChoices.SCHEDULED,
    )
