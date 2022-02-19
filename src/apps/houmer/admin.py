from django.contrib import admin
from .models import Houmer
from .models import ScheduledVisit
from .models import ScheduledVisitEvent


@admin.register(Houmer)
class HoumerAdmin(admin.ModelAdmin):
    pass


@admin.register(ScheduledVisit)
class ScheduledVisitAdmin(admin.ModelAdmin):
    pass


@admin.register(ScheduledVisitEvent)
class ScheduledVisitEventAdmin(admin.ModelAdmin):
    pass
