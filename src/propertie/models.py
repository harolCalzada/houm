from django.db import models
from django.contrib.gis.db.models import PointField


class Propertie(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=2)
    location = PointField()

    def __str__(self):
        return f'{self.name} - {self.price}'