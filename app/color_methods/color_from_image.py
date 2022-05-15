from backend.app.color_methods.color_name import ColorName
from backend.app.color_methods.segmented_image import SegmentedImage


class ColorFromImage:

    def __init__(self, img, precise_color_detection):
        self.image = img
        if not precise_color_detection:
            segmented_image = SegmentedImage()
            self.image = segmented_image.get_segmented_image(img)

    def find_color(self, x, y):
        """
        Finds information about a color on an image with specified coordinates.

        :param x:
        :param y:
        :return color information:
        """
        blue = self.image[y, x, 0]
        green = self.image[y, x, 1]
        red = self.image[y, x, 2]
        rgb = (int(red), int(green), int(blue))
        color_name = ColorName()
        return {'rgb': (red, green, blue),
                'color': color_name.convert_rgb_to_name(rgb),
                'hue': color_name.find_hue_name(rgb)}
