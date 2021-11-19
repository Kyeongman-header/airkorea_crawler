from django.contrib import admin
from .models import *
from django.contrib.gis.admin import OSMGeoAdmin
# Register your models here

class GPSAdmin(OSMGeoAdmin):
    list_display=('pub_date','gps')
    list_filter=['pub_date','gps']
    search_fields=['pub_date','gps']
class AirKoreaAdmin(admin.ModelAdmin):
    list_display=('pub_date','airkorea')
    list_filter=['pub_date','airkorea']
    search_fields=['pub_date','airkorea']

admin.site.register(GPS,GPSAdmin)
admin.site.register(AirKorea,AirKoreaAdmin)


