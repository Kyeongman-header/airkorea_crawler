from .models import *
from rest_framework import serializers

class GPSSerializer(serializers.ModelSerializer):
    class Meta:
        model=GPS
        fields=['gps','pub_date']

class AirKoreaSerializer(serializers.ModelSerializer):
    class Meta:
        model=AirKorea
        fields=['airkorea','pub_date']
