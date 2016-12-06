import sys
import csv
import requests
import json
from PIL import Image,ImageDraw,ImageFont
from region import Region,get_state,get_us,mercator
from plot import Plot, color
import re
from hospitals import *

MAX_RADIUS = 100
IMG_SIZE = 3000

def state_map(state,DRGcode,width,parameter):
    """
    Produces map of state(s) with a circle for each hospital with size corresponding to the number of discharges and color corresponding to the average medicare reimbursement
    Arguments:
        state = list of 2 capital letter strings
        DRGcode = str
        width = int
        filename = str.png
        parameter = "M","P","T" or "C"
            M = medicare payment
            P = difference between total payment and medicare payment
            T = total payment
            C = covered charges
    """
    regions = get_state(state)

    min_long = min([reg.min_long() for reg in regions])
    min_lat = min([reg.min_lat() for reg in regions])
    max_long = max([reg.max_long() for reg in regions])
    max_lat = max([reg.max_lat() for reg in regions])
    print("Boundary Data Collected")

    p = Plot(width,min_long,min_lat,max_long,max_lat)

    for county in regions:
        p.draw_boundary(county)
    print("State Boundary Drawn")

    hosplist = order_hospitals(get_hospitals(state,DRGcode))
    print("Hospital List Assembled")
    min_val = min_parameter(hosplist,parameter)
    max_val = max_parameter(hosplist,parameter)

    if parameter == "M":
        for h in hosplist:
            if h.coords():
                radius = MAX_RADIUS*(h.discharges()/max_discharge(hosplist))
                circle_color = color(h.medicare(),min_val,max_val)
                p.draw_circle(h.coords(),circle_color,radius)
    elif parameter == "C":
        for h in hosplist:
            if h.coords():
                radius = MAX_RADIUS*(h.discharges()/max_discharge(hosplist))
                circle_color = color(h.charge(),min_val,max_val)
                p.draw_circle(h.coords(),circle_color,radius)
    elif parameter == "T":
        for h in hosplist:
            if h.coords():
                radius = MAX_RADIUS*(h.discharges()/max_discharge(hosplist))
                circle_color = color(h.totalpay(),min_val,max_val)
                p.draw_circle(h.coords(),circle_color,radius)
    elif parameter == "P":
        for h in hosplist:
            if h.coords():
                radius = MAX_RADIUS*(h.discharges()/max_discharge(hosplist))
                circle_color = color(h.paydiff(),min_val,max_val)
                p.draw_circle(h.coords(),circle_color,radius)

    print("Circles Drawn")
    filename = "{}_{}_{}.png".format(state,DRGcode,parameter)
    p.save(filename)

def region_map(statelist,DRGcode,width,parameter):
    """
    Produces map of state(s) with a circle for each hospital with size corresponding to the number of discharges and color corresponding to the average medicare reimbursement
    Arguments:
        statelist = list of 2 capital letter strings
        DRGcode = str
        width = int
        filename = str.png
        parameter = "M","P","T" or "C"
            M = medicare payment
            P = difference between covered charges and total payment
            T = total payment
            C = covered charges
    """
    regions = []
    for state in statelist:
        regions = regions + get_state(state)
    print("Boundary Data Collected")

    min_long = min([reg.min_long() for reg in regions])
    min_lat = min([reg.min_lat() for reg in regions])
    max_long = max([reg.max_long() for reg in regions])
    max_lat = max([reg.max_lat() for reg in regions])

    p = Plot(width,min_long,min_lat,max_long,max_lat)

    for county in regions:
        p.draw_boundary(county)
    print("Map Drawn")

    hosplist = []
    for state in statelist:
        hosplist = hosplist + get_hospitals(state,DRGcode)
        print("State Hospital List Collected")
    hosplist = order_hospitals(hosplist)
    print("Hospital List Complete")

    min_val = min_parameter(hosplist,parameter)
    max_val = max_parameter(hosplist,parameter)

    if parameter == "M":
        for h in hosplist:
            if h.coords():
                radius = MAX_RADIUS*(h.discharges()/max_discharge(hosplist))
                circle_color = color(h.medicare(),min_val,max_val)
                p.draw_circle(h.coords(),circle_color,radius)
    elif parameter == "C":
        for h in hosplist:
            if h.coords():
                radius = MAX_RADIUS*(h.discharges()/max_discharge(hosplist))
                circle_color = color(h.charge(),min_val,max_val)
                p.draw_circle(h.coords(),circle_color,radius)
    elif parameter == "T":
        for h in hosplist:
            if h.coords():
                radius = MAX_RADIUS*(h.discharges()/max_discharge(hosplist))
                circle_color = color(h.totalpay(),min_val,max_val)
                p.draw_circle(h.coords(),circle_color,radius)
    elif parameter == "P":
        for h in hosplist:
            if h.coords():
                radius = MAX_RADIUS*(h.discharges()/max_discharge(hosplist))
                circle_color = color(h.paydiff(),min_val,max_val)
                p.draw_circle(h.coords(),circle_color,radius)

    print("Circles Drawn")
    filename = "{}_{}_{}.png".format("".join(statelist),DRGcode,parameter)
    p.save(filename)

def us_map(DRGcode,width,parameter):
    """
    Produces map of the US with a circle for each hospital with size corresponding to the number of discharges and color corresponding to the average medicare reimbursement
    Arguments:
        DRGcode = str
        width = int
        filename = str.png
        parameter = "M","P","T" or "C"
            M = medicare payment
            P = difference between covered charges and total payment
            T = total payment
            C = covered charges

    Note: I am not completely sure this function is making complete visualizations. I am concerned the program is overwhelmed by storing the list of hospital object for all the hospitals in the US. The program need to be run more too determine whats going on (each run takes about 20-30min)
    """
    regions = get_us()
    print("Boundary Data Collected")

    min_long = min([reg.min_long() for reg in regions])
    min_lat = min([reg.min_lat() for reg in regions])
    max_long = max([reg.max_long() for reg in regions])
    max_lat = max([reg.max_lat() for reg in regions])

    p = Plot(width,min_long,min_lat,max_long,max_lat)

    for county in regions:
        p.draw_boundary(county)
    print("US Drawn")

    STATELIST = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]

    master_list = dict()
    min_values = []
    max_values = []
    max_discharges = []

    for state in STATELIST:
        hosplist = order_hospitals(get_hospitals(str(state),str(DRGcode)))
        print("Hospital List Ordered")
        master_list[state] = hosplist
        min_values.append(min_parameter(hosplist,parameter))
        print(min_values)
        max_values.append(max_parameter(hosplist,parameter))
        max_discharges.append(max_discharge(hosplist))
        print("State Hospital List Created")

    min_val = min(min_values)
    max_val = max(max_values)
    max_disch = max(max_discharges)
    print("Hospital Data Collected")

    max_discharge
    for state in STATELIST:
        hosplist = master_list[state]
        if parameter == "M":
            for h in hosplist:
                if h.coords():
                    radius = MAX_RADIUS*(h.discharges()/max_disch)
                    circle_color = color(h.medicare(),min_val,max_val)
                    p.draw_circle(h.coords(),circle_color,radius)
        elif parameter == "C":
            for h in hosplist:
                if h.coords():
                    radius = MAX_RADIUS*(h.discharges()/max_disch)
                    circle_color = color(h.charge(),min_val,max_val)
                    p.draw_circle(h.coords(),circle_color,radius)
        elif parameter == "T":
            for h in hosplist:
                if h.coords():
                    radius = MAX_RADIUS*(h.discharges()/max_disch)
                    circle_color = color(h.totalpay(),min_val,max_val)
                    p.draw_circle(h.coords(),circle_color,radius)
        elif parameter == "P":
            for h in hosplist:
                if h.coords():
                    radius = MAX_RADIUS*(h.discharges()/max_disch)
                    circle_color = color(h.paydiff(),min_val,max_val)
                    p.draw_circle(h.coords(),circle_color,radius)
        print("State Complete: {}".format(state))

    filename = "US_{}_{}.png".format(DRGcode,parameter)
    p.save(filename)

if __name__ == '__main__':
    if sys.argv[1] == '1':
        if str(sys.argv[2]) != "US":
            state_map(str(sys.argv[2]),str(sys.argv[3]),IMG_SIZE,str(sys.argv[4]))
        else:
            us_map(str(sys.argv[3]),IMG_SIZE,str(sys.argv[4]))

    else:
        n = int(sys.argv[1])
        statelist = [str(sys.argv[i]) for i in range(2,2+n+1)]
        region_map(statelist,str(sys.argv[2+n]),IMG_SIZE,str(sys.argv[3+n]))
