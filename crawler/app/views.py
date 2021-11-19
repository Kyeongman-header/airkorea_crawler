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

import requests
import datetime
# Create your views here.

def find_airkorea(gps):
    # json 파싱한 데이터를 받는 거니까 이미 string일듯.
    gps=gps.split(';')[1]
    # 단 앞에 좌표게 정보 SRID=4326;이 있으므로 ;를 구분자로 하여 파싱해주고 뒤에 있는 놈을 취하면 됨.
    
    default_location_url='http://api.vworld.kr/req/data?service=data&request=GetFeature&data=LT_C_ADSIGG_INFO&key=FEA696B3-DA29-3EC5-95F3-5272C2CD83B5&'
    geomFilter='geomFilter=' + gps
    res=requests.get(default_location_url+geomFilter)
    
    if res.status_code != 200 :
        print(res.text)
        return None
        
    location=res.json()['response']['result']['featureCollection']['features'][0]['properties']['sig_kor_nm']
    default_airkorea_url='http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?serviceKey=i%2BZcNpR8%2BTbY%2BB%2FEXAV6qnMCBHmgcfwzcEfA%2Fap8vqckk%2BDn%2FvZDzgeaT28h95%2BhacFHs8Chrfkr2Bb4gILtsw%3D%3D&returnType=json&ver=1.3&dataTerm=DAILY&'
    stationName='stationName=' + location
    res=requests.get(default_airkorea_url+stationName)
    if res.status_code !=200:
        print(res.text)
        return None
    
    return (res.json()['response']['body']['items'][0]['pm25Value'])


@csrf_exempt
def gps(request):
    #if request.user.is_admin:
    if request.method == "POST":
        data=JSONParser().parse(request)
        serializer1=GPSSerializer(data=data)
        if serializer1.is_valid():

            serializer1.save()
            # 이 저장 기능은 로그 기능을 위한 것으로, 그것도 어차피 개발 단계의 디버깅을 위한 것이다.
            #자체적으로 기간이 오래된 데이터는 삭제해주는 기능이 필요하다.

            airkorea=find_airkorea(serializer1.data['gps'])
            if airkorea != None:
                ak=AirKorea.objects.create(airkorea=airkorea)
                serializer2=AirKoreaSerializer(ak)

                serializer2.save()
                # 이 저장 기능 역시 마찬가지이다. 

                return JsonResponse(serializer2.data,status=201)

        return JsonResponse(serializer1.errors,status=400)
    return HttpResponse(status=405)
    #return HttpResponse(status=401)

