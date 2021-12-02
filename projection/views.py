from django.shortcuts import render
import math
import json
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from common import astroFunction
from common.astroFunction import routePoints


def home_page(request):
    homePagePath = 'home.html'
    context = {'Message' : 'Home Page'}
    return render(request, 'home.html', context)

def astro_projection(request):
    context = {}
    return render(request, 'astroProjection.html', context)

class JSONResponse(HttpResponse):
    def __init__(self,data,**kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse,self).__init__(content,**kwargs)

@csrf_exempt
@api_view(['GET','POST'])
def getTripPoints(request, startPoint, endPoint, distApart):
    lat1 = float(startPoint.split(",")[0])
    lon1 = float(startPoint.split(",")[1])
    lat2 = float(endPoint.split(",")[0])
    lon2 = float(endPoint.split(",")[1])
    distApart = int(distApart)
    
    context = {}
    jsResult = json.dumps(routePoints(lat1, lon1, lat2, lon2, distApart))
    return JSONResponse(jsResult)
