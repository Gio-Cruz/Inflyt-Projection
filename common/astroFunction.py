import math
from datetime import datetime as dt
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
    
    print(d)
    
    for distance in range(0, d, distApart):
        waypoints.append(waypoint(theta1, lamb1, delta, distance))
    
    print(waypoints)
    return waypoints

#routePoints(45,60, 45, 30, 100)
print(dt.utcnow().time())

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
def JulianDay():
    Y = dt.today().year
    M = dt.today().month
    D = dt.today().day
    
    if M <= 2:
        M, Y = M+2, Y-1
    A = int(Y/100)
    B = 2 - A + int(A/4)
    JD = int(365.25*(Y+4716)) + int(30.6001*(M+1)) + D - B - 1524.5
    return JD
    
# convert decimal degrees to hr min sec
def ToHrMinSec(deg):
    Hr = int(deg/15) # 15 arc degrees = 1 hour
    Min = int(((deg/15) - Hr)*60) 
    Sec = ((((deg/15) - Hr)*60) - Min)*60
    return [Hr, Min, Sec]
    
# convert geocentric latitude/longitude to right ascension and declination
def GeoToCelestial(lat,long):
    long = float(long)
    dec = DecimalToDMS(lat)
    JD = JulianDay()
    T = (JD - 2451545)/36525
    # calculate mean sidereal time at greenwich
    theta0 = 280.46061837 + 360.98564736629*(JD - 2451545.0) + 0.000387933*T*T - (T*T*T)/ 38710000
    while theta0 >= 360:
        theta0 -= 360
    LST = theta0 + long
    # convert deg to hr-min-sec
    ra = ToHrMinSec(LST)
    #print("Right Acension = {}hr {}min {}s, Declination = {}° {}' {}\"".format(ra[0],ra[1],ra[2], dec[0],dec[1],dec[2]))
    return ra, dec
    
#GeoToCelestial(36.7783, -119.4179)


    
    
    
    
    
    
    
    
    
    
    
    
    