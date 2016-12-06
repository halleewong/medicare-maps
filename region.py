import csv
import math

class Region:
    """
    A region (represented by a list of (long,lat) coordinates)
    """
    def __init__(self, coords):
        self.coords = coords

    def lats(self):
        "Return a list of the latitudes (y) of all the coordinates in the region"
        return [y for (x,y) in self.coords]

    def longs(self):
        "Return a list of the longitudes (x) of all the coordinates in the region"
        return [x for (x,y) in self.coords]

    def min_lat(self):
        "Return the minimum latitude (y) of the region"
        return min(self.lats())

    def min_long(self):
        "Return the minimum longitude (x) of the region"
        return min(self.longs())

    def max_lat(self):
        "Return the maximum latitude (y) of the region"
        return max(self.lats())

    def max_long(self):
        "Return the maximum longitude (x) of the region"
        return max(self.longs())

def mercator(lat):
    """
    project latitude 'lat' according to Mercator
    """
    lat_rad = (lat * math.pi) / 180
    projection = math.log(math.tan((math.pi / 4) + (lat_rad / 2)))
    return (180 * projection) / math.pi

def to_point(lst):
    """
    Takes a list of coordinates and returns a list of coordinate tuples that have been projected
    """
    new_lst = []
    if len(lst) % 2 == 0:
        for i in range(0,len(lst),2):
            new_lst.append((float(lst[i]),mercator(float(lst[i+1]))))
    else:
        return "List is incomplete"
    return new_lst

def get_state(state):
    """
    Returns a list of region objects for each county in state "AZ"
    """
    states = list(csv.reader(open("boundaries/US.csv",'r')))
    counties = []
    for row in states:
        if row[1] == state:
            counties.append(Region(to_point(row[2:])))
    return counties

def get_us():
    """
    Returns a list of region objects for every county in the US
    """
    states = list(csv.reader(open("boundaries/US.csv",'r')))
    counties = []
    for row in states:
        counties.append(Region(to_point(row[2:])))
    return counties
