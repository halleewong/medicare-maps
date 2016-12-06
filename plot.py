from PIL import Image, ImageDraw, ImageFont
from PIL.ImageColor import getrgb
from region import Region
import copy

def color(val,min,max,reverse=False):
    """
    Returns an appropriate RGBA color given a value and a minimum and maximum where large numbers are green and small numbers are red
    if reverse=TRUE:
            Large values -> green
            Small values -> red
    if reverse=FALSE:
        Large values -> red
        Small values -> Green
    """
    if val == 0.5*(max-min)+min:
        #White
        return (255,255,255,255)
    if val < 0.5*(max-min)+min:
        #small value
        m = abs(val - (0.5*(max-min)+min))/(0.5*(max-min))
        if reverse:
            #Green
            return (255-int(m*(255-88)),255-int(m*(255-214)),255-int(m*(255-141)),255)
        else:
            #Red
            return (255-int(m*(255-231)),255-int(m*(255-76)),255-int(m*(255-60)),255)

    if val > 0.5*(max-min)+min:
        #large value
        m = abs((0.5*(max-min)+min) - val)/(0.5*(max-min))
        if reverse:
            #Red
            return (255-int(m*(255-231)),255-int(m*(255-76)),255-int(m*(255-60)),255)
        else:
            #Green
            return (255-int(m*(255-88)),255-int(m*(255-214)),255-int(m*(255-141)),255)


class Plot:
    """
    Provides the ability to map, draw and color regions in a long/lat
    bounding box onto a proportionally scaled image.
    """
    @staticmethod
    def interpolate(x_1,x_2,x_3,newlength):
        """
        linearly interpolates x_2 <= x_1 <= x_3 into [0,newlength]
        x_2 and x_3 define a line segment, and x2 falls somewhere between them
        scale the width of the line segment to newlength, and return where
        x_1 falls on the scaled line.
        """
        return int(newlength * (x_1 - x_2) / (x_3 - x_2))

    @staticmethod
    def proportional_height(new_width,width,height):
        """return a height for new_width that is
        proportional to height with respect to width
        Yields: int: a new height
        """
        return int(new_width * height / width)

    @staticmethod
    def trans_coord(coords,min_long,min_lat,max_long,max_lat,width,height):
        """
        Interpolate longitudinal/latiudinal values into image coordinates
        """
        longs = [Plot.interpolate(x, min_long, max_long, width) for (x,y) in coords]
        lats = [Plot.interpolate(max_lat - (y - min_lat), min_lat, max_lat, height) for (x,y) in coords]
        return [(x,y) for (x,y) in zip(longs,lats)]

    def __init__(self,width,min_long,min_lat,max_long,max_lat):
        """
        Create a width x height image where height is proportional to width with respect to the long/lat coordinates.
        """
        self.im = Image.new("RGBA",(width,Plot.proportional_height(width, max_long - min_long,max_lat - min_lat)), (255,255,255))
        self.width = width
        self.height = Plot.proportional_height(width,max_long - min_long, max_lat - min_lat)
        self.min_long = min_long
        self.min_lat = min_lat
        self.max_long = max_long
        self.max_lat = max_lat

    def save(self, filename):
        """
        save the current image to 'filename'
        """
        self.im.save(filename, "PNG")

    def draw_boundary(self,region,RGBA=(214,234,248,255)):
        """
        Draws 'region' at the correct position on the current image
        Args:
            region (Region) = a Region object with a set of coordinates
        """
        coords = Plot.trans_coord(
                    region.coords,
                    self.min_long,
                    self.min_lat,
                    self.max_long,
                    self.max_lat,
                    self.width,
                    self.height)
        ImageDraw.Draw(self.im).polygon(coords,fill=RGBA,outline=None)

    def draw_circle(self,hosp_coords,RGBAinterior,radius):
        """
        Draw a circle in at the correct position on the current image
        Arguments:
            hosp_coords = list of hospital coordinates (x,y)
            RGBAinterior = RGBA color (int,int,int,int)
            radius = integer
        """
        if hosp_coords:
            r = float(radius)
            for (x,y) in Plot.trans_coord(hosp_coords,self.min_long,
            self.min_lat,self.max_long,self.max_lat,self.width,self.height):
                ImageDraw.Draw(self.im).ellipse([x-r,y-r,x+r,y+r],
                fill=RGBAinterior,outline=(255,255,255,255))

    def draw_legend_circle(self,coords,RGBAinterior,radius):
        """
        Draw a circle in at the correct position on the current image
        Arguments:
            coords = coordinates (x,y)
            RGBAinterior = RGBA color (int,int,int,int)
            radius = integer
        """
        r = float(radius)
        x = coords[0]
        y = coords[1]
        ImageDraw.Draw(self.im).ellipse([x-r,y-r,x+r,y+r],
            fill=RGBAinterior,outline=(255,255,255,255))

    def draw_legend(self,max_discharges,min_val,max_val,MAX_RADIUS):

        inc = (max_val-min_val)/6
        self.draw_legend_circle((MAX_RADIUS,self.height-MAX_RADIUS),color(max_val,min_val,max_val),MAX_RADIUS)
        self.draw_legend_circle((MAX_RADIUS,self.height-0.6*MAX_RADIUS),color(max_val-inc,min_val,max_val),0.6*MAX_RADIUS)
        self.draw_legend_circle((MAX_RADIUS,self.height-0.3*MAX_RADIUS),color(max_val-2*inc,min_val,max_val),0.3*MAX_RADIUS)

        font = ImageFont.truetype('Arial.ttf',24)
        ImageDraw.Draw(self.im).text((MAX_RADIUS,self.height-2*MAX_RADIUS-50),str(max_discharges),font=font,fill=(0,0,0,255))
        ImageDraw.Draw(self.im).text((MAX_RADIUS,self.height-1.2*MAX_RADIUS-50),str(0.6*max_discharges),fill=(0,0,0,255),font=font)
