import colorsys

from colormath.color_diff import delta_e_cie2000

from backend.app.color_methods.color_converter import ColorConverter
from backend.app.color_methods.color_name import ColorName


class ColorHarmony:

    def __init__(self):
        self.color_converter = ColorConverter()

    def get_analogous_distance(self, val1, val2):
        """
        Finds the minimum distance between one selected color's harmonious colors (based on analogous harmony) and
        the second color.

        :param val1:
        :param val2:
        :return distance:
        """
        ana_val = self.get_analogous_colors(val1)

        lab_val = self.color_converter.rgb_to_lab(val2)
        lab_ana_1 = self.color_converter.rgb_to_lab(ana_val[0])
        lab_ana_2 = self.color_converter.rgb_to_lab(ana_val[1])

        d1 = self.get_delta_e(lab_val, lab_ana_1)
        d2 = self.get_delta_e(lab_val, lab_ana_2)

        if d1 < d2:
            return d1
        else:
            return d2

    def get_complimentary_distance(self, val1, val2):
        """
        Finds the distance between one selected color's harmonious color (based on complimentary harmony) and
        the second color.

        :param val1:
        :param val2:
        :return distance:
        """
        comp_val = self.get_complimentary_colors(val1)

        lab_val = self.color_converter.rgb_to_lab(val2)
        lab_comp = self.color_converter.rgb_to_lab(comp_val)

        return self.get_delta_e(lab_val, lab_comp)

    def get_monochromatic_distance(self, val1, val2):
        """
        Finds the minimum distance between one selected color's harmonious colors (based on monochromatic harmony) and
        the second color.

        :param val1:
        :param val2:
        :return distance:
        """
        mono_val = self.get_monochromatic_colors(val2)

        lab_val = self.color_converter.rgb_to_lab(val1)

        result = 1000

        for mono in mono_val:
            lab_mono = self.color_converter.rgb_to_lab(mono)
            distance = self.get_delta_e(lab_val, lab_mono)
            if distance < result:
                result = distance

        return result

    def get_neutral_color_distance(self, val1, val2):
        """
        Finds whether one of the colors is harmonious. If either of the inputted colors is a neutral color (black, white,
        gray), the colors are harmonious and the distance between one of the inputted colors and its harmonious
        correspondent is 0 (minimum distance), otherwise the result is 100 (maximum distance).

        :param val1:
        :param val2:
        :return:
        """
        color_name = ColorName()
        color_name_1 = color_name.find_hue_name(val1)
        color_name_2 = color_name.find_hue_name(val2)

        neutral_colors = ["Black", "White", "Gray"]

        if color_name_1 in neutral_colors or color_name_2 in neutral_colors:
            return 0
        return 100

    def get_analogous_colors(self, rgb):
        """
        Finds the chosen RGB code's analogous colors.

        Used source: https://thingsgrow.me/2020/01/02/navigating-through-000000-and-ffffff-color-theory-in-python/
        :param rgb:
        :return list of analogous colors:
        """
        analogous_colors = []
        degrees = 60 / 360.0
        h, l, s = self.color_converter.rgb_to_hls(rgb)
        hues_60_deg = ((h - degrees) % 1, (h + degrees) % 1)
        for hue in hues_60_deg:
            analogous_color = tuple(map(lambda x: round(x * 255), colorsys.hls_to_rgb(hue, l, s)))
            analogous_colors.append(analogous_color)
        return analogous_colors

    def get_complimentary_colors(self, rgb):
        """
        Find's the chosen RGB code's complimentary color.

        Used source: https://thingsgrow.me/2020/01/02/navigating-through-000000-and-ffffff-color-theory-in-python/
        :param rgb:
        :return complimentary color:
        """
        h, l, s = self.color_converter.rgb_to_hls(rgb)
        hue_180_deg = h + (180.0 / 360.0)
        complimentary_color = tuple(map(lambda x: round(x * 255), colorsys.hls_to_rgb(hue_180_deg, l, s)))
        return complimentary_color

    def get_monochromatic_colors(self, rgb):
        """
        Finds the chosen RGB code's monochromatic colors.

        :param rgb:
        :return list of monochromatic colors:
        """
        h, l, s = self.color_converter.rgb_to_hls(rgb)

        increment = [0, 0.05, 0.10]
        result = [rgb]
        for i in increment:
            for j in increment:
                rgb1 = list(map(lambda x: round(x * 255), colorsys.hls_to_rgb(h, l + i, s + j)))
                rgb2 = list(map(lambda x: round(x * 255), colorsys.hls_to_rgb(h, l - i, s - j)))
                result.append(self.get_positive_rgb(rgb1))
                result.append(self.get_positive_rgb(rgb2))
        return list(set(result))

    def get_positive_rgb(self, rgb):
        """
        Changes all RGB code values into positive numbers

        :param rgb:
        :return rgb with positive values:
        """
        res = []
        for i in rgb:
            if i < 0:
                i = 256 - i
            res.append(i)
        return tuple(res)

    def get_delta_e(self, lab1, lab2):
        """
        Find the delta e distance between two chosen colors.

        :param lab1:
        :param lab2:
        :return distance:
        """

        return round(delta_e_cie2000(lab1, lab2))
