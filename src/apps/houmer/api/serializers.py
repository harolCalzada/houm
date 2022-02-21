from rest_framework import serializers
from ..models import ScheduledVisit, ScheduledVisitEvent, ScheduledVisitStatistic


class ScheduledVisitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledVisit
        fields = "__all__"
        read_only_fields = [
            'houmer',
            'status',
            'created_at',
            'modified_at'
        ]


class ScheduledVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledVisit
        fields = "__all__"


class ScheduledVisitStatusSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = ScheduledVisit
        fields = ['id', 'status', 'latitude', 'longitude', 'houmer', 'propertie']
        read_only_fields = ['houmer', 'id', 'propertie']


class ScheduledVisitEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledVisitEvent
        fields = "__all__"


class ScheduleVisitDetailSerializer(serializers.ModelSerializer):
    scheduled_visit_events = ScheduledVisitEventSerializer(many=True, read_only=True)

    class Meta:
        model = ScheduledVisit
        fields = [
            'id',
            'houmer',
            'scheduled_date_at',
            'propertie',
            'activity',
            'status',
            'created_at',
            'modified_at',
            'scheduled_visit_events',
        ]
        read_only_fields = [
            'houmer',
            'id',
            'scheduled_date_at',
            'propertie',
            'activity',
            'status',
            'created_at',
            'modified_at'
        ]


class scheduledVisitStatisticSerializer(serializers.ModelSerializer):
    property_location = serializers.SerializerMethodField()

    class Meta:
        model = ScheduledVisitStatistic
        fields = "__all__"

    def get_property_location(self, obj):
        location = obj.schedule_visit.propertie.location
        return f'{location.y}, {location.x}'
