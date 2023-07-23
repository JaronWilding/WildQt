"""
    Global class and function definitions for LAQtUi.
    Contains functions and classes that are used by multiple tools.
    ---
    Classes include:
        - ClickableLabel
        - ColourPicker
        - QHLine
        - QVLine
"""

# TODO: Add docstrings to all classes and functions.

# For changelog
__author__ = "Jaron Wilding"
__version__ = "1.0.0"
__date__ = "07/18/2023"
__status__ = "Release"

# Python imports
import re
import colorsys
from enum import Enum

# Maya imports
try:
    import maya.api.OpenMaya as om2 # type: ignore
    Maya = True
except:
    Maya = False

class Colour(Enum):
    RGB = 0
    RGBFull = 1
    HSV = 2
    HEX = 3
    HEXLONG = 4
    CMY = 5
    CMYK = 6


class LAColour(object):
    """A custom colour class that can be used to store and convert Colour between different colour spaces.

    There are no error checks for invalid values, by design so nothing get's in the way of the user.
    Note: CMYK comes with a 5th value, alpha, which is not used in the conversion to RGB.
    ---
    Public methods:
        - get (colour_space): Returns the colour in the specified colour space. 
            If no colour space is specified, the colour is returned in the colour space it was created in.
        - set (colour, colour_space): Sets the colour to the specified colour space. 
            If no colour space is specified, the colour is set in the colour space it was created in.
    """

    def __init__(self, colour=[0.0, 0.0, 0.0, 1.0], colour_space=Colour.RGB, clamped=True):
        self._colour_space = colour_space
        self._clamp_values = clamped
        self._colour = [0.0, 0.0, 0.0, 1.0]
        self.set(colour, colour_space)


    def get(self, colour_space=None):
        # type: (Colour) -> list | str
        """Returns the colour in the specified colour space.
        If no colour space is specified, the colour is returned in the colour space it was created in.
        Note: HSV returns the hue as an int, and the saturation and value as a percentage.
        
        Args:
            - colour_space (Colour): The colour space to return the colour in.
        """

        colour_space = self._colour_space if colour_space is None else colour_space
        if colour_space is Colour.RGB:
            return self._getRGB()
        if colour_space is Colour.RGBFull:
            return self._getRGBFull()
        if colour_space is Colour.HSV:
            return self._getHSV()
        if colour_space is Colour.CMYK:
            return self._getCMYK()
        if colour_space is Colour.HEX or colour_space is Colour.HEXLONG:
            return self._getHEX(colour_space)
    
    def set(self, colour=None, colour_space=None):
        # type: (list | str, Colour) -> None
        """Sets the colour to the specified colour space.
        If no colour space is specified, the colour is set in the colour space it was created in.
        Note: HSV takes the hue as an int, and the saturation and value as a percentage.
        
        Args:
            - colour (list | str): The colour to set.
            - colour_space (Colour): The colour space to set the colour in.
        """

        colour = self._colour if colour is None else colour
        if colour_space is Colour.RGB:
            self._setRGB(*colour)
        elif colour_space is Colour.RGBFull:
            self._setRGBFull(*colour)
        elif colour_space is Colour.HSV:
            self._setHSV(*colour)
        elif colour_space is Colour.CMYK:
            self._setCMYK(*colour)
        elif colour_space is Colour.HEX or colour_space is Colour.HEXLONG:
            self._setHEX(colour)

        return self.get(colour_space=colour_space)
    
    def _clamp(self, val, minVal, maxVal):
        return max(min(val, maxVal), minVal) if self._clamp_values else val
    
    def _getRGB(self):
        return self._colour
    
    def _setRGB(self, r=0.0, g=0.0, b=0.0, a=1.0):
        self._colour = [self._clamp(x, 0.0, 1.0) for x in [r, g, b, a]]

    def _getRGBFull(self):
        colour = [int(x * 255.0) for x in self._colour[0:3]]
        colour.append(self._colour[3])
        return colour
    
    def _setRGBFull(self, r=0.0, g=0.0, b=0.0, a=1.0):
        self._setRGB(r / 255.0, g / 255.0, b / 255.0, a)

    def _getHSV(self):
        r, g, b = self._colour[0:3]
        Cmax = max(self._colour[0:3])
        Cmin = min(self._colour[0:3])

        delta = Cmax - Cmin
        if Cmax == Cmin:
            hue = 0
        elif Cmax == r:
            hue = 60 * (((g - b) / delta) % 6)
        elif Cmax == g:
            hue = 60 * (((b - r) / delta) + 2)
        elif Cmax == b:
            hue = 60 * (((r - g) / delta) + 4)

        sat = 0 if Cmax == 0 else delta / Cmax

        return [int(hue), int(sat * 100), int(Cmax * 100), self._colour[3]]

    def _setHSV(self, h=0.0, s=0.0, v=0.0, a=1.0):
        s = s * 0.01
        v = v * 0.01
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        if h <= 0 or h < 60:
            r, g, b = c, x, 0
        elif h <= 60 or h < 120:
            r, g, b = x, c, 0
        elif h <= 120 or h < 180:
            r, g, b = 0, c, x
        elif h <= 180 or h < 240:
            r, g, b = 0, x, c
        elif h <= 240 or h < 300:
            r, g, b = x, 0, c
        elif h <= 300 or h < 360:
            r, g, b = c, 0, x

        self._colour = [(r+m), (g+m), (b+m), a]

    def _getCMYK(self):
        K = 1 - max(self._colour[0:3])
        cmyk = [int(((1 - x - K) / (1 - K)) * 100.0) for x in self._colour[0:3]]
        cmyk.append(self._colour[3])
        return cmyk

    def _setCMYK(self, c=0.0, m=0.0, y=0.0, k=0.0, a=1.0):
        _k = (1 - k * 0.01)
        self._colour = [(1 - c * 0.01) * _k, (1 - m * 0.01) * _k, (1 - y * 0.01) * _k , a]

    def _getHEX(self, colour_space):
        if colour_space is Colour.HEX:
            return "{:02x}{:02x}{:02x}".format(*[int(x * 255.0) for x in self._colour[0:3]])
        return "{:02x}{:02x}{:02x}{:02x}".format(*[int(x * 255.0) for x in self._colour])

    def _setHEX(self, hex):
        # type: (str, Colour) -> None
        hex = hex.replace("#", "").lower()
        if len(hex) == 6:
            self._colour = [int(hex[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
            self._colour.append(1.0)
            return
        if len(hex) == 8:
            self._colour = [int(hex[i:i+2], 16) / 255.0 for i in (0, 2, 4, 6)]
            return
    

class LAMColour(LAColour):
    def __init__(self, colour=[0.0, 0.0, 0.0, 1.0], colour_space=Colour.RGB, clamped=True):
        super(LAMColour, self).__init__(colour, colour_space, clamped)
        
    def set(self, colour=None, colour_space=None):
        self.m_colour = om2.MColor()
        super(LAMColour, self).set(colour, colour_space)
        

    def _getRGB(self):
        return self.m_colour.getColor(om2.MColor.kRGB)
    
    def _setRGB(self, r=0.0, g=0.0, b=0.0, a=1.0):
        self.m_colour.setColor([r, g, b, a], om2.MColor.kRGB)
    
    def _getRGBFull(self):
        rgb = self._getRGB()
        return [int(x * 255.0) for x in rgb]
    
    def _setRGBFull(self, r=0.0, g=0.0, b=0.0, a=1.0):
        self._setRGB(r / 255.0, g / 255.0, b / 255.0, a)

    def _getHSV(self):
        return self.m_colour.getColor(om2.MColor.kHSV)
    
    def _setHSV(self, h=0.0, s=0.0, v=0.0, a=1.0):
        self.m_colour.setColor([h, s, v, a], om2.MColor.kHSV)

    def _getCMY(self):
        return self.m_colour.getColour(om2.MColor.kCMY)
    
    def _setCMY(self, c=0, m=0, y=0, a=1):
        self.m_colour.setCMYColor([c, m, y, a], om2.MColor.kCMY)

    def _getCMYK(self):
        return self.m_colour.getColour(om2.MColor.kCMYK)
    
    def _setCMYK(self, c=0, m=0, y=0, k=0, a=1):
        self.m_colour.setCMYKColor([c, m, y, k], om2.MColor.kCMYK)
        self.m_colour.a = a

    def _getHEX(self, colour_space):
        rgb = self._getRGBFull()
        if colour_space is Colour.HEX:
            return "{:02x}{:02x}{:02x}".format(*rgb[0:3])
        return "{:02x}{:02x}{:02x}{:02x}".format(*rgb)

    def _setHEX(self, hex) -> None:
        hex = hex.replace("#", "").lower()
        if re.match(r"^(([0-9A-Fa-f]{2}){3,4}|[0-9A-Fa-f]{3})$", hex):
            if len(hex) == 6:
                self._colour = [int(hex[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
                self._colour.append(1.0)
            elif len(hex) == 8:
                self._colour = [int(hex[i:i+2], 16) / 255.0 for i in (0, 2, 4, 6)]

            self._setRGB(*self._colour)
        
