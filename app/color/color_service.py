import base64
from datetime import datetime

import cv2
import numpy as np
from flask import jsonify

from app.color_methods.color_converter import ColorConverter
from app.color_methods.color_from_image import ColorFromImage
from app.color.color_repository import ColorRepository
from app.models import Color


class ColorService:

    def __init__(self):
        self.color_repository = ColorRepository()

    def find_color(self, img, precise, x, y):
        x = round(x)
        y = round(y)
        new_data = img.replace('data:image/png;base64,', '').replace('data:image/jpeg;base64,', '')
        im_bytes = base64.b64decode(new_data)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
        actual_image = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

        color_from_image = ColorFromImage(actual_image, precise)
        color = color_from_image.find_color(x, y)

        return jsonify({'rgb': str(color.get('rgb')), 'color': color.get('color'), 'hue': color.get('hue')})

    def get_colors(self):
        lst = []
        color_converter = ColorConverter()
        colors = self.color_repository.get_colors()
        for color in colors:
            if color.displayable:
                lst.append({'id': color.id,
                            'name': color.name,
                            'rgb': str(color_converter.hex_to_rgb(color.hex_code)),
                            'hue': color.hue,
                            'date': str(color.date),
                            'comment': color.comment})
        return jsonify(lst)

    def add_color(self, name, rgb, hue, comment, displayable):
        color_converter = ColorConverter()
        hex_code = color_converter.rgb_to_hex(rgb).replace("#", "")
        date = datetime.now()
        color = Color(name=name, hex_code=hex_code, date=date, hue=hue, displayable=displayable, comment=comment)
        self.color_repository.add_color(color)
        return jsonify({'success': True})

    def update_color(self, color_id, comment):
        # raise Exception('general exceptions not caught by specific handling')
        self.color_repository.update_color(color_id, comment)
        return jsonify({'success': True})

    def delete_color(self, color_id):
        color = self.color_repository.get_color(color_id)
        color_harmonies_ids = color.color_palettes
        self.color_repository.delete_color(color, color_harmonies_ids)
        return jsonify({'success': True})
