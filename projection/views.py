from django.shortcuts import render
import math
import json
from django.contrib.staticfiles.views import serve
from projection import services
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from common import astroFunction
from common.astroFunction import routePoints, GeoToCelestial
from astroquery.simbad import Simbad
from astroquery.simbad.core import SimbadVOTableResult
from astropy.io.votable import parse
import astropy.coordinates as coord
import astropy.units as u


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

def getCelestial(request, lat, long):
        print("in getCelestial lat/long: {} {}".format(lat,long))
        ra, dec = GeoToCelestial(lat, long)
        print("In GetCelestial: {},{}".format(ra, dec))
        raString = str(ra[0])+ " " + str(ra[1]) + " " + str(round(ra[2],2))
        decString = str(dec[0])+ " " + str(dec[1]) + " " + str(round(dec[2],2))
        #print (raString + " +" + decString)
        #c = coord.SkyCoord(raString + " +" + decString , unit=(u.hourangle, u.deg) )
        #print(c)
        #result = Simbad.query_region_async(coord.SkyCoord(raString + " +" + decString , unit=(u.hourangle, u.deg), frame='icrs' ), radius='0d10m0s')
        #tableResult = SimbadVOTableResult(result.text, verbose=True).table['MAIN_ID']
        #for row in tableResult :
            #print (row)
        
        resultDict = {"ra" : raString, "dec" : decString}
        print(resultDict)
        context = {}
        jsResult = json.dumps(resultDict)
        return JSONResponse(jsResult)
        


def getIDNames(request, ra, dec):
    ra = ra.split(" ")
    dec = dec.split(" ")
    ra_str = ra[0]+"h"+ra[1]+"m"+ra[2]+"s"
    dec_str = dec[0]+"d"+dec[1]+"m"+dec[2]+"s"

    resultDict = services.get_object_ids(ra_str, dec_str)
    #print(resultDict)
    context = {}
    jsResult = json.dumps(resultDict)
    return JSONResponse(jsResult)


