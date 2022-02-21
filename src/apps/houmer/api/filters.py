from django_filters import rest_framework as filters
from apps.houmer.models import ScheduledVisitStatistic


class ScheduledVisitsStatisticFilter(filters.FilterSet):
    velocity_km_x_h = filters.NumberFilter(field_name="velocity_km_x_h", lookup_expr="gte")
    stay_time_in_minutes = filters.NumberFilter(field_name="stay_time_in_minutes", lookup_expr="gte")

    class Meta:
        model = ScheduledVisitStatistic
        fields = (
            "date",
            "velocity_km_x_h",
            "stay_time_in_minutes",
            "schedule_visit__activity"
        )
