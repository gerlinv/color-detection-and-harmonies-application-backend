import pandas as pd

from app.color_methods.color_converter import ColorConverter
from app.resources import color_HSL_ranges


class ColorName:

    def __init__(self):
        """
        colors.csv source: https://github.com/codebrainz/color-names/blob/master/output/colors.csv
        """
        index = ["color", "color_name", "hex", "R", "G", "B"]
        self.csv = pd.read_csv('app/resources/colors.csv', names=index, header=None)
        self.hue_dictionary = color_HSL_ranges.color_dict_HSV

    def convert_rgb_to_name(self, rgb):
        """
        A method that converts an RGB code to its name correspondent.

        Used source: https://medium.com/programming-fever/color-detection-using-opencv-python-6eec8dcde8c7
        :param rgb:
        :return color name:
        """
        r, g, b = rgb
        minimum = 10000
        color_name = ""
        for i in range(len(self.csv)):
            distance = abs(r - int(self.csv.loc[i, "R"])) + \
                       abs(g - int(self.csv.loc[i, "G"])) + \
                       abs(b - int(self.csv.loc[i, "B"]))
            if distance <= minimum:
                minimum = distance
                color_name = self.csv.loc[i, "color_name"]
        return color_name

    def find_hue_name(self, rgb):
        """
        A method that converts an RGB code to it's corresponding hue.

        :param rgb:
        :return hue:
        """
        color_converter = ColorConverter()
        hsv = color_converter.rgb_to_hsv(rgb)
        for i in range(len(self.hue_dictionary)):
            upper_range = self.hue_dictionary[i][1][0]
            lower_range = self.hue_dictionary[i][1][1]
            color_in_range = True
            for j in range(3):
                if lower_range[j] > hsv[j] or hsv[j] > upper_range[j]:
                    color_in_range = False
            if color_in_range:
                result = ''.join(k for k in self.hue_dictionary[i][0] if not k.isdigit())
                return result
