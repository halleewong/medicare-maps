import sys
import csv
import requests
import json
from region import Region,get_state,get_us,mercator
from plot import Plot
import re

DRGCOL = 0
STATECOL = 5
ADDRESSCOL = 3
CITYCOL = 4
DISCHARGECOL = 8
CHARGECOL = 9
TOTALPAYCOL = 10
MEDICARECOL = 11

APIKEY = "AIzaSyBYk-MV1UztIdpDvO9AvrW2svNFm3u49w4"
#"AIzaSyDtOHsktbLWsCQdkJqjqSDkImQ0_ajgs48"

class Hospital:

    def __init__(self,DRGcode,address,city,state,discharges,charge,totalpay,medicare):
        """
        address = street address of the Hospital
        city = city where the hospital is located
        state = state where the hospital is located
        dischages = number of discharges billed in FY2011 (for specific DRG code and hospital)
        charge = the hospital's average charge for this service (DRG)
        totalpay = average total reimbursement hospital recieves for this DRG
        medicare = average medicare reimbursement hospital recieves for this DRG
        """
        self._address = address
        self._city = city
        self._state = state
        self._drg = DRGcode
        self._discharges = discharges
        self._charge = charge
        self._totalpay = totalpay
        self._medicare = medicare
        self._paydiff = 0
        self._coords = ()

    @staticmethod
    def filter_address(text):
        """
        Some address are in the form "#### & ### Some St", which confuses the google maps Geocoding api. This function corrects those address to be "### Some St".
        """
        if "&" in text:
            REGEX = '''& ([\w ]*)'''
            address = re.search(REGEX,text)
            return address.group(1)
        else:
            return text

    @staticmethod
    def filter_money(text):
        """
        Takes string of the form '$XX,XXX.XX' and returns a float
        """
        REGEX = '''\$([0-9]{,3}),?([0-9]{3}.[0-9]{2})'''
        value = re.search(REGEX,text)
        return float(value.group(1) + value.group(2))

    @staticmethod
    def address_to_coords(address,city,state):
        """
        Convert street addresses to (longitude,latitude)
        """
        url = "https://maps.googleapis.com/maps/api/geocode/json?address={},+{},+{}&key={}".format("+".join(Hospital.filter_address(address).split()),"+".join(city.split()),state,APIKEY)
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            print(url)
            print(address)
            location_dict = json.loads(r.text)
            if location_dict['status'] == "OK":
                if location_dict['results'][0]['geometry']['location']['lng']:
                    longitude = location_dict['results'][0]['geometry']['location']['lng']
                    latitude = location_dict['results'][0]['geometry']['location']['lat']
                    #print(longitude,latitude)
                    return [(longitude,mercator(latitude))]
        else:
            return None

    def populate_coords(self):
        """
        Populates self._coords and self._paydiff
        """
        self._coords = Hospital.address_to_coords(self._address,self._city,self._state)
        self._paydiff = self._charge - self._totalpay

    def coords(self):
        """
        Returns the (latitude,longitude) coordinates of the hospital
        """
        return self._coords

    def discharges(self):
        """
        Returns the number of discharges
        """
        return int(self._discharges)

    def medicare(self):
        """
        Returns the average medicare reimbursement
        """
        return float(self._medicare)

    def charge(self):
        """
        Returns the average covered charges
        """
        return float(self._charge)

    def paydiff(self):
        """
        Returns the average paydiff
        """
        return float(self._paydiff)

    def totalpay(self):
        """
        Returns the average total payment
        """
        return float(self._totalpay)

def get_hospitals(state,DRGcode):
    """
    Make Hospital objects of all hospitals in 'state' with 'DRGcode' with their coordinates
    """
    hosplist = []
    with open('hospitaldata.csv','r') as fin:
        data = list(csv.reader(fin))
        for row in data[1:]:
            if row[DRGCOL].startswith(DRGcode) and row[STATECOL].strip() == state:
                hosplist.append(Hospital(DRGcode,row[ADDRESSCOL],row[CITYCOL],row[STATECOL],int(row[DISCHARGECOL]),Hospital.filter_money(row[CHARGECOL]),Hospital.filter_money(row[TOTALPAYCOL]),Hospital.filter_money(row[MEDICARECOL])))
                print("Object Made")
    for hospital in hosplist:
        hospital.populate_coords()
        print("Hospital geocoded")
    return hosplist

def get_all_hospitals(DRGcode):
    """
    Make Hospital objects of all hospitals in 'state' with 'DRGcode' with their coordinates
    """
    hosplist = []
    print("IS HERE")
    with open('hospitaldata.csv','r') as fin:
        data = list(csv.reader(fin))
        for row in data[1:]:
            if row[DRGCOL].startswith(DRGcode):
                hosplist.append(Hospital(DRGcode,row[ADDRESSCOL],row[CITYCOL],row[STATECOL],int(row[DISCHARGECOL]),Hospital.filter_money(row[CHARGECOL]),Hospital.filter_money(row[TOTALPAYCOL]),Hospital.filter_money(row[MEDICARECOL])))
    for hospital in hosplist:
        hospital.populate_coords()
        print("Hospital geocoded")
    return hosplist

def max_discharge(hosplist):
    """
    Finds the maximum discharges among hospitals in a list
    hosplist = list of Hospital objects
    """
    lst = []
    for hospital in hosplist:
        lst.append(hospital.discharges())
    return max(lst)

def order_hospitals(hosplist):
    """
    Ordered a list of Hospital objects by the number of discharges from largest to smallest
    """
    d = {}
    for hospital in hosplist:
        d[hospital.discharges()] = hospital
    return [d[key] for key in sorted(d,reverse=True)]

def min_parameter(hosplist,parameter):
    """
    Finds the minimum value of parameter amoung hospital objects in a list
    hosplist = list of Hospital objects
    """
    if parameter == "M": #Medicare
        return min([h.medicare() for h in hosplist])
    elif parameter == "P": #Paydifference
        return min([h.paydiff() for h in hosplist])
    elif parameter == "C": #Charge
        return min([h.charge() for h in hosplist])
    elif parameter == "T": #totalpay
        return min([h.totalpay() for h in hosplist])

def max_parameter(hosplist,parameter):
    """
    Finds the maximum value of parameter amoung hospital objects in a list
    hosplist = list of Hospital objects
    """
    if parameter == "M": #Medicare
        return max([h.medicare() for h in hosplist])
    elif parameter == "P": #Paydifference
        return max([h.paydiff() for h in hosplist])
    elif parameter == "C": #Charge
        return max([h.charge() for h in hosplist])
    elif parameter == "T": #totalpay
        return max([h.totalpay() for h in hosplist])
