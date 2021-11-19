from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.parsers import JSONParser

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login


from .models import *
from .serializers import *
#from .permissions import *


import datetime
# Create your views here.

def find_airkorea(gps):
    return None


@csrf_exempt
def gps(request):
    if request.user.is_admin:
        if request.method == "POST":
            data=JSONParser().parse(request)
            serializer1=GPSSerializer(data=data)
            if serializer1.is_valid():
                serializer1.save()
                airkorea=find_airkorea(serializer1.data['gps'])
                if airkorea != None:
                    ak=AirKorea.objects.create(airkorea=airkorea)
                    serializer2=AirKoreaSerializer(ak)
                    serializer2.save()
                    return JsonResponse(serializer2.data,status=201)

            return JsonResponse(serializer1.errors,status=400)
        return HttpResponse(status=405)
    return HttpResponse(status=401)

