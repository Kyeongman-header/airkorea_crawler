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


from pyproj import Proj, transform

def find_airkorea(gps):
    # json 파싱한 데이터를 받는 거니까 이미 string일듯.
    gps=gps.split(';')[1]
    gps=gps.replace('(','')
    gps=gps.replace(')','')
    xy=gps.split(' ')
    X=xy[1]
    Y=xy[2]

    # 단 앞에 좌표게 정보 SRID=4326;이 있으므로 ;를 구분자로 하여 파싱해주고 뒤에 있는 놈을 취하면 됨.
   
    proj_GRS80=Proj(init='epsg:5181')
    proj_WGS84=Proj(init='epsg:4326')
    X2,Y2=transform(proj_WGS84,proj_GRS80,float(X),float(Y))
    loc_airkorea_url='http://apis.data.go.kr/B552584/MsrstnInfoInqireSvc/getNearbyMsrstnList?serviceKey=i%2BZcNpR8%2BTbY%2BB%2FEXAV6qnMCBHmgcfwzcEfA%2Fap8vqckk%2BDn%2FvZDzgeaT28h95%2BhacFHs8Chrfkr2Bb4gILtsw%3D%3D&returnType=json&'
    TM_xy='tmX='+str(X2)+'&tmY='+str(Y2)
    res=requests.get(loc_airkorea_url+TM_xy)
    if res.status_code !=200:
        print(res.text)
        return None
    
    location=res.json()['response']['body']['items'][0]['stationName']

    default_airkorea_url='http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?serviceKey=i%2BZcNpR8%2BTbY%2BB%2FEXAV6qnMCBHmgcfwzcEfA%2Fap8vqckk%2BDn%2FvZDzgeaT28h95%2BhacFHs8Chrfkr2Bb4gILtsw%3D%3D&returnType=json&ver=1.3&dataTerm=DAILY&'
    stationName='stationName=' + location
    res=requests.get(default_airkorea_url+stationName)
    if res.status_code !=200:
        print(res.text)
        return None

    airkorea_datas=res.json()['response']['body']['items'][0]
    Flags={'so2Flag' : False,'coFlag' : False,'o3Flag' : False,'no2Flag' : False,'pm25Flag' : False,'khaiFlag' : False}
    Flags['so2Flag']= False if airkorea_datas['so2Flag']==None else True
    Flags['coFlag']= False if airkorea_datas['coFlag']==None else True
    Flags['o3Flag']= False if airkorea_datas['o3Flag']==None else True
    Flags['no2Flag']= False if airkorea_datas['no2Flag']==None else True
    Flags['pm25Flag']= False if airkorea_datas['pm25Flag']==None else True
    Flags['khaiFlag']= False if airkorea_datas['khaiFlag']==None else True
    
    return location, float(res.json()['response']['body']['items'][0]['so2Value']) if airkorea_datas['so2Flag']==None else 0, float(res.json()['response']['body']['items'][0]['coValue']) if airkorea_datas['coFlag']==None else 0, float(res.json()['response']['body']['items'][0]['o3Value']) if airkorea_datas['o3Flag']==None else 0,float(res.json()['response']['body']['items'][0]['no2Value']) if airkorea_datas['no2Flag']==None else 0,float(res.json()['response']['body']['items'][0]['pm25Value']) if airkorea_datas['pm25Flag']==None else 0,float(res.json()['response']['body']['items'][0]['khaiValue']) if airkorea_datas['khaiFlag']==None else 0



@csrf_exempt
def gps(request):
    #if request.user.is_admin:
    X=request.GET.get('X',None)
    Y=request.GET.get('Y',None)
    point='SRID=4326;POINT (' + X + ' ' + Y + ')'
    gps={'gps':point}
    location,so2,co,o3,no2,pm2_5,khai=find_airkorea(point)

    d={'gps':point,'location':location}

    serializer1=GPSSerializer(data=d)

        #data=JSONParser().parse(request)
        #serializer1=GPSSerializer(data=data)
    if serializer1.is_valid():

        serializer1.save()
            # 이 저장 기능은 로그 기능을 위한 것으로, 그것도 어차피 개발 단계의 디버깅을 위한 것이다.
            #자체적으로 기간이 오래된 데이터는 삭제해주는 기능이 필요하다.

        if (so2 != None) and (co != None) and (o3 != None) and (no2 != None) and (pm2_5 != None) and (khai != None) :
            d={ "airkorea" : {"P.M 2.5" : pm2_5, "CO" : co, "SO2" : so2, "O3" : o3, "NO2" : no2, "khai" : khai }}
            serializer2=AirKoreaSerializer(data=d)
            if serializer2.is_valid():
                serializer2.save()
                return JsonResponse(serializer2.data,status=201)
            return JsonResponse(serializer2.errors,status=400)
        return HttpResponse(status=501)
    return JsonResponse(serializer1.errors,status=400)

