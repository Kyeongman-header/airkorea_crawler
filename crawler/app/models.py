from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.conf import settings


# Create your models here

class GPS(models.Model):
    gps=models.PointField()
    location=models.CharField(default="unknown",max_length=20,null=True,blank=True)
    pub_date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.gps)

class AirKorea(models.Model):
    now=timezone.now()
    airkorea=models.JSONField()
    pub_date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.airkorea)
