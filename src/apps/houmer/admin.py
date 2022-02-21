from django.contrib import admin
from .models import Houmer
from .models import ScheduledVisit, ScheduledVisitEvent, ScheduledVisitStatistic


@admin.register(Houmer)
class HoumerAdmin(admin.ModelAdmin):
    pass


@admin.register(ScheduledVisit)
class ScheduledVisitAdmin(admin.ModelAdmin):
    pass


@admin.register(ScheduledVisitEvent)
class ScheduledVisitEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'scheduled_visit', 'current_status', 'position']


@admin.register(ScheduledVisitStatistic)
class ScheduledVisitStatisticAdmin(admin.ModelAdmin):
    pass
