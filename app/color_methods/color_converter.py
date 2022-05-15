import colorsys

from colormath.color_conversions import convert_color
from colormath.color_objects import sRGBColor, LabColor


class ColorConverter:

    def __init__(self):
        pass

    def rgb_to_hex(self, rgb):
        """
        Converts RGB to HEX.

        :param rgb:
        :return hex:
        """
        return '#%02x%02x%02x' % rgb

    def hex_to_rgb(self, hex):
        """
        Converts HEX to RGB.

        Used source: https://thingsgrow.me/2020/01/02/navigating-through-000000-and-ffffff-color-theory-in-python/
        :param hex:
        :return rgb:
        """
        hex_value = hex.strip('#')
        hex_length = len(hex_value)
        conversion = tuple(int(hex_value[i:i + hex_length // 3], 16) for i in range(0, hex_length, hex_length // 3))
        return conversion

    def rgb_to_hls(self, rgb):
        """
        Converts RGB to HLS.

        :param rgb:
        :return hls:
        """
        r, g, b = map(lambda x: x / 255.0, rgb)
        return colorsys.rgb_to_hls(r, g, b)

    def rgb_to_lab(self, rgb):
        """
        Converts RGB to L*a*b.

        :param rgb:
        :return lab:
        """
        r, g, b = rgb
        srgb = sRGBColor(r, g, b, is_upscaled=True)
        return convert_color(srgb, LabColor, target_illuminant='D50')

    def rgb_to_hsv(self, rgb):
        """
        Converts RGB to HSV.

        :param rgb:
        :return hsv:
        """
        r, g, b = map(lambda x: x / 255.0, rgb)
        hsv_percentage = list(colorsys.rgb_to_hsv(r, g, b))
        h = round(180 * hsv_percentage[0])
        s = round(255 * hsv_percentage[1])
        v = round(255 * hsv_percentage[2])
        return h, s, v
