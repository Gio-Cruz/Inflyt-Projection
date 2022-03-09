import math
from datetime import datetime as dt
import time
#from cffi.backend_ctypes import long

R = 6371.0

def waypoint(theta, lamb, delta, dis):
    t2 = math.asin( math.sin(theta) * math.cos(dis/R) + math.cos(theta) * math.sin(dis/R) * math.cos(delta))
    l2 = lamb + math.atan2( math.sin(delta) * math.sin(dis/R) * math.cos(theta) , math.cos(dis/R) - math.sin(theta) * math.sin(t2))
    l2 = (l2 + 3 * math.pi) % (2 * math.pi) - math.pi
    return [math.degrees(t2), math.degrees(l2)]

def routePoints(startLat, startLon, endLat, endLon, distApart):
    theta1 , lamb1 = math.radians(startLat) , math.radians(startLon)
    theta2 , lamb2 = math.radians(endLat), math.radians(endLon)
    
    d = R * math.acos( math.sin(theta1) * math.sin(theta2) + math.cos(theta1) * math.cos(theta2) * math.cos(lamb2 - lamb1))
    d = int(d)
    
    delta = math.atan2( math.sin(lamb2 - lamb1) * math.cos(theta2), math.cos(theta1) * math.sin(theta2) - math.sin(theta1) * math.cos(theta2) * math.cos(lamb2 - lamb1))
    
    
    waypoints = []
    
    #print(d)
    
    for distance in range(0, d, distApart):
        waypoints.append(waypoint(theta1, lamb1, delta, distance))
    
    #print(waypoints)
    return waypoints

#routePoints(45,60, 45, 30, 100)


########################################################################################################################################
def absFloor(val):
    if (val >= 0.0):
        return math.floor(val)
    else: 
        return math.ceil(val)
    
def modDay(val):
    b = val/24.0
    a = 24.0*(b-absFloor(b))
    if (a < 0): 
        a = a + 24.0
    #print("modDay: {}".format(a))
    return a

def mod2pi(angle):
    b = angle/360.0
    a = 360.0*(b-absFloor(b))
    if (a < 0):
        a = a + 360.0
    #print("mod2pi: {}".format(a))
    return a

def getDaysinMonth(mm, yy):
    mm = int(mm)
    yy = int(yy)
    ndays = 31
    if ((mm == 4) or (mm==6) or (mm==9) or (mm==11)):
        ndays = 30;
    if (mm == 2):
        ndays = 28
        if ((yy % 4) == 0):
            ndays = 29
        if ((yy % 100) == 0):
            ndays = 28
        if ((yy % 400) == 0):
            ndays = 29;
    return ndays

# convert degrees minutes seconds to decimal degrees
def DMSToDecimal(hr, m, s):
    return hr + (m/60.0) + (s/60)

def DecimalToDMS(deg):
    deg = float(deg)
    degrees = int(deg)
    m = (deg-degrees)*60
    s = (m-int(m))*60
    m = int(m)
    return [degrees, m, s]

# return Julian Date for current UTC
def JulianDay(yy,mm,dd,hh):
    yy = float(yy)
    mm = float(mm)
    dd = float(dd)
    hh = float(hh) 
    extra = (100.0*yy + mm) - 190002.5;
    jday  = 367.0*yy;
    jday -= math.floor(7.0*(yy+math.floor((mm+9.0)/12.0))/4.0);
    jday += math.floor(275.0*mm/9.0);
    jday += dd;
    jday += hh/24.0;
    jday += 1721013.5;
    jday -= 0.5*extra/abs(extra);
    jday += 0.5;
    return jday
    
def getDayno2K(yy,mm,dd,hh):
    jd = JulianDay(yy,mm,dd,hh)
    return jd - 2451543.5

def calcLST(olong):
    lsign = 1.0
    hr = round(dt.today().hour + dt.today().minute/60.0, 2)
    month = dt.today().month
    day = dt.today().day
    year = dt.today().year
    tzone = -1.0*time.timezone/3600
    if olong > 180:
        olong = olong - 180
        olong = abs(olong)
    hemi = "W" if tzone < 0.0 else "E"
    if hemi == "W":
        lsign = -1.0
    
    ut = modDay(hr - tzone)
    dno = getDayno2K(year, month, day, hr)
    ws = mod2pi(282.9404 + 4.70935*math.pow(10.0,-5)*dno)
    ms = mod2pi(356.0470 + 0.9856002585*dno)
    #print(dno)
    meanlong = mod2pi(ms + ws)
    gmst0 = (meanlong)/15.0
    lst = modDay(gmst0 + ut + lsign*olong/15.0) + 11.0 + 56.0/60.0
    #print("gmst0: "+str(gmst0) + "ut: "+str(ut)+"lsign: "+str(lsign)+"olong: "+str(olong))
    if (lst >= 24.0): 
        lst = lst - 24.0
    return lst
# convert decimal degrees to hr min sec
def ToHrMinSec(hrs):
    Hr = int(hrs) # 15 arc degrees = 1 hour
    Min = int((hrs-Hr)*60) 
    Sec = (((hrs - Hr)*60) - Min)*60
    return [Hr, Min, Sec]
    
# convert geocentric latitude/longitude to right ascension and declination
def GeoToCelestial(lat,long):
    long = float(long)
    dec = DecimalToDMS(lat)
    LST = calcLST(long)
    print(LST)
    # convert deg to hr-min-sec
    ra = ToHrMinSec(LST)
    #print("Right Acension = {}hr {}min {}s, Declination = {}° {}' {}\"".format(ra[0],ra[1],ra[2], dec[0],dec[1],dec[2]))
    return ra, dec
    
ra, dec = GeoToCelestial(120, 120)

#print(ra,dec)


    
    
    
