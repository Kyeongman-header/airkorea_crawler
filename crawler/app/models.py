from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.conf import settings


# Create your models here

class GPS(models.Model):
    now=timezone.now()
    gps=models.PointField()
    pub_date=models.DateTimeField(default=now)

    def __str__(self):
        return str(self.gps)

class AirKorea(models.Model):
    now=timezone.now()
    airkorea=models.JSONField()
    pub_date=models.DateTimeField('airkorea date published',default=now)
    def __str__(self):
        return str(self.airkorea)
