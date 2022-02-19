from rest_framework import serializers
from ..models import ScheduledVisit


class ScheduledVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledVisit
        fields = "__all__"

