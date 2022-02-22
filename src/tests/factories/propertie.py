from django.contrib.gis.geos import Point
from django.conf import settings
from apps.propertie.models import Propertie


def propertie_factory(
    name: str,
    description: str,
    location_latitude: float,
    location_longitude: float,
    price: float = 1000000,
) -> Propertie:
    return Propertie.objects.create(
        name=name,
        description=description,
        price=price,
        location=Point(
            location_latitude,
            location_longitude,
            srid=settings.SRID
        )
    )
