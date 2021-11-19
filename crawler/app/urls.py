from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import url,include

urlpatterns=[
    path('api/gps/',views.gps, name='gps'),
]
