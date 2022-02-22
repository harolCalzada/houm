
from http import HTTPStatus
from django.contrib.gis.geos import Point
from django.conf import settings
from apps.houmer.choices import ActivityChoices, StatusChoices
from apps.houmer.models import ScheduledVisit, ScheduledVisitEvent, ScheduledVisitStatistic


def test_create_scheduled_visit(api_client, houmer_a, propertie_a):
    api_client.force_authenticate(user=houmer_a)
    data = {
        "scheduled_date_at": "2022-02-21T16:58:32.039Z",
        "activity": ActivityChoices.TOUR,
        "propertie": propertie_a.id
    }
    response = api_client.post('/api/houmer/scheduled-visit/', data)
    assert response.status_code == HTTPStatus.CREATED
    scheduled_visit_id = response.json()['id']
    scheduled_visit_instance = ScheduledVisit.objects.get(id=scheduled_visit_id)
    assert scheduled_visit_instance.houmer == houmer_a
    assert scheduled_visit_instance.propertie == propertie_a
    assert scheduled_visit_instance.activity == ActivityChoices.TOUR
    assert scheduled_visit_instance.status == StatusChoices.SCHEDULED


def test_scheduled_visit_change_status_to_in_transit(api_client, houmer_a, scheduled_visit_to_property_a):
    api_client.force_authenticate(user=houmer_a)
    id_scheduled_visit = scheduled_visit_to_property_a.id
    data = {
        "new_status": StatusChoices.IN_TRANSIT,
        "latitude": -11.9151,
        "longitude": -77.0478
    }
    response = api_client.put(
        f'/api/houmer/scheduled-visit/{id_scheduled_visit}/',
        data=data,
        format='json'
    )
    assert response.status_code == HTTPStatus.OK
    scheduled_visit_id = response.json()['id']
    scheduled_visit_instance = ScheduledVisit.objects.get(id=scheduled_visit_id)
    assert scheduled_visit_instance.status == StatusChoices.IN_TRANSIT


def test_change_status_to_in_progress(api_client, houmer_a, scheduled_visit_to_property_a):
    api_client.force_authenticate(user=houmer_a)
    id_scheduled_visit = scheduled_visit_to_property_a.id
    # changed status to in transit
    scheduled_visit_to_property_a.in_transit(0, 0)
    scheduled_visit_to_property_a.save()
    data = {
        "new_status": StatusChoices.IN_PROGRESS,
        "latitude": -11.9151,
        "longitude": -77.0478
    }
    response = api_client.put(
        f'/api/houmer/scheduled-visit/{id_scheduled_visit}/',
        data=data,
        format='json'
    )
    assert response.status_code == HTTPStatus.OK
    scheduled_visit_id = response.json()['id']
    scheduled_visit_instance = ScheduledVisit.objects.get(id=scheduled_visit_id)
    assert scheduled_visit_instance.status == StatusChoices.IN_PROGRESS


def test_change_status_to_completed(api_client, houmer_a, scheduled_visit_to_property_a):
    api_client.force_authenticate(user=houmer_a)
    id_scheduled_visit = scheduled_visit_to_property_a.id
    # changed status to in progress
    scheduled_visit_to_property_a.in_transit(0, 0)
    scheduled_visit_to_property_a.in_progress(0, 0)
    scheduled_visit_to_property_a.save()
    data = {
        "new_status": StatusChoices.COMPLETED,
        "latitude": -11.9151,
        "longitude": -77.0478
    }
    response = api_client.put(
        f'/api/houmer/scheduled-visit/{id_scheduled_visit}/',
        data=data,
        format='json'
    )
    assert response.status_code == HTTPStatus.OK
    scheduled_visit_id = response.json()['id']
    scheduled_visit_instance = ScheduledVisit.objects.get(id=scheduled_visit_id)
    assert scheduled_visit_instance.status == StatusChoices.COMPLETED


def test_invalid_status_change(api_client, houmer_a, scheduled_visit_to_property_a):
    api_client.force_authenticate(user=houmer_a)
    id_scheduled_visit = scheduled_visit_to_property_a.id
    data = {
        "new_status": StatusChoices.COMPLETED,
        "latitude": -11.9151,
        "longitude": -77.0478
    }
    response = api_client.put(
        f'/api/houmer/scheduled-visit/{id_scheduled_visit}/',
        data=data,
        format='json'
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    scheduled_visit_instance = ScheduledVisit.objects.get(id=id_scheduled_visit)
    assert scheduled_visit_instance.status == StatusChoices.SCHEDULED


def test_status_changed_to_in_transit_side_effects(houmer_a, scheduled_visit_to_property_a):
    origin_coordinates = (-11.9151, -77.0478)
    # changed status to in transit
    scheduled_visit_to_property_a.in_transit(*origin_coordinates)
    scheduled_visit_to_property_a.save()
    event_in_progress_instance = ScheduledVisitEvent.objects.get(
        scheduled_visit=scheduled_visit_to_property_a,
        current_status=StatusChoices.IN_TRANSIT
    )
    scheduled_visit_statistic = ScheduledVisitStatistic.objects.get(
        schedule_visit=scheduled_visit_to_property_a
    )
    assert event_in_progress_instance
    assert event_in_progress_instance.position == Point(*origin_coordinates, srid=settings.SRID)
    assert scheduled_visit_statistic


def test_status_changed_to_in_progress_side_effects(houmer_a, scheduled_visit_to_property_a):
    origin_coordinates = (-11.9151, -77.0478)
    target_coordinates = (-12.1234, -77.0478)
    # changed status to in progress
    scheduled_visit_to_property_a.in_transit(*origin_coordinates)
    scheduled_visit_to_property_a.in_progress(*target_coordinates)
    scheduled_visit_to_property_a.save()
    event_in_progress_instance = ScheduledVisitEvent.objects.get(
        scheduled_visit=scheduled_visit_to_property_a,
        current_status=StatusChoices.IN_PROGRESS
    )
    scheduled_visit_statistic = ScheduledVisitStatistic.objects.get(
        schedule_visit=scheduled_visit_to_property_a
    )
    assert event_in_progress_instance
    assert event_in_progress_instance.position == Point(*target_coordinates, srid=settings.SRID)
    assert scheduled_visit_statistic
    assert scheduled_visit_statistic.velocity_km_x_h


def test_status_changed_to_completed_side_effects(houmer_a, scheduled_visit_to_property_a):
    origin_coordinates = (-11.9151, -77.0478)
    target_coordinates = (-12.1234, -77.0478)
    # changed status to in completed
    scheduled_visit_to_property_a.in_transit(*origin_coordinates)
    scheduled_visit_to_property_a.in_progress(*target_coordinates)
    scheduled_visit_to_property_a.completed(*target_coordinates)
    scheduled_visit_to_property_a.save()
    event_in_progress_instance = ScheduledVisitEvent.objects.get(
        scheduled_visit=scheduled_visit_to_property_a,
        current_status=StatusChoices.COMPLETED
    )
    scheduled_visit_statistic = ScheduledVisitStatistic.objects.get(
        schedule_visit=scheduled_visit_to_property_a
    )
    assert event_in_progress_instance
    assert event_in_progress_instance.position == Point(*target_coordinates, srid=settings.SRID)
    assert scheduled_visit_statistic
    assert scheduled_visit_statistic.velocity_km_x_h
    assert scheduled_visit_statistic.stay_time_in_minutes is not None