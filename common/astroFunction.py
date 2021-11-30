import math

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