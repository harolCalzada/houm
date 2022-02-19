from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import ScheduledVisit
from .serializers import ScheduledVisitSerializer


class ScheduledVisitViewSet(viewsets.ModelViewSet):
    queryset = ScheduledVisit.objects.all()
    serializer_class = ScheduledVisitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ScheduledVisit.objects.all()
        return ScheduledVisit.objects.filter(houmer=user)
