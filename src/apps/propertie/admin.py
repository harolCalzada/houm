from django.contrib import admin
from .models import Propertie


@admin.register(Propertie)
class PropertieAdmin(admin.ModelAdmin):
    pass
