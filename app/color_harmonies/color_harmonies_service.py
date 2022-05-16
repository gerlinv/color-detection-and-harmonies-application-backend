from datetime import datetime

from flask import jsonify

from app.color_methods.color_converter import ColorConverter
from app.color_methods.color_harmony import ColorHarmony
from app.color.color_repository import ColorRepository
from app.color.color_service import ColorService
from app.color_harmonies.color_harmonies_repository import ColorHarmoniesRepository
from app.models import ColorPalette


class ColorHarmoniesService:

    def __init__(self):
        self.color_harmonies_repository = ColorHarmoniesRepository()
        self.color_repository = ColorRepository()
        self.color_service = ColorService()

    def calculate_harmonies(self, val1, val2):
        color_harmony = ColorHarmony()
        ana = color_harmony.get_analogous_distance(val1, val2)
        comp = color_harmony.get_complimentary_distance(val1, val2)
        mono = color_harmony.get_monochromatic_distance(val1, val2)
        base = color_harmony.get_neutral_color_distance(val1, val2)

        return jsonify({'ana': ana, 'comp': comp, 'mono': mono, 'neutral': base})

    def get_harmonies(self, harmonies_id):
        harmonies = self.color_harmonies_repository.get_harmonies(harmonies_id)
        color_ids = harmonies.colors
        c1 = self.color_repository.get_color(color_ids[0].id)
        if len(color_ids) == 1:
            c2 = c1
        else:
            c2 = self.color_repository.get_color(color_ids[1].id)
        color_converter = ColorConverter()
        val1 = {
            'name': c1.name,
            'rgb': str(color_converter.hex_to_rgb(c1.hex_code)),
            'hue': c1.hue,
            'date': str(c1.date),
            'comment': c1.comment
        }
        val2 = {
            'name': c2.name,
            'rgb': str(color_converter.hex_to_rgb(c2.hex_code)),
            'hue': c2.hue,
            'date': str(c2.date),
            'comment': c2.comment
        }
        return jsonify({'val1': val1, 'val2': val2})

    def get_all_harmonies(self):
        color_palettes = self.color_harmonies_repository.get_all_harmonies()
        lst = []
        color_palette_ids = []
        for color_palette in color_palettes:
            if color_palette.id not in color_palette_ids:
                lst.append({
                    'id': color_palette.id,
                    'date': str(color_palette.date),
                    'ana': color_palette.analogous_harmony,
                    'comp': color_palette.complimentary_harmony,
                    'mono': color_palette.monochromatic_harmony,
                    'neutral': color_palette.neutral_color_harmony,
                    'comment': color_palette.comment
                })
                color_palette_ids.append(color_palette.id)
        return jsonify(lst)

    def add_harmonies(self, rgb1, rgb2, name1, name2, hue1, hue2, ana, comp, mono, neutral, comment):
        color_converter = ColorConverter()
        val1_hex = color_converter.rgb_to_hex(rgb1).replace("#", "")
        val2_hex = color_converter.rgb_to_hex(rgb2).replace("#", "")

        colors = self.color_repository.get_color_descending_id()
        val1_exists = None
        val2_exists = None
        for color in colors:
            if color.hex_code == val1_hex:
                val1_exists = color
            if color.hex_code == val2_hex:
                val2_exists = color

        if val1_exists is None:
            self.color_service.add_color(name1, rgb1, hue1, None, False)
            val1_exists = colors.first()
        if val2_exists is None:
            self.color_service.add_color(name2, rgb2, hue2, None, False)
            val2_exists = colors.first()

        date = datetime.now()
        if val1_exists == val2_exists:
            colors = [val1_exists]
        else:
            colors = [val1_exists, val2_exists]
        harmonies = ColorPalette(colors=colors,
                                 analogous_harmony=ana,
                                 complimentary_harmony=comp,
                                 monochromatic_harmony=mono,
                                 neutral_color_harmony=neutral,
                                 date=date,
                                 comment=comment)
        self.color_harmonies_repository.add_harmonies(harmonies)

        return jsonify({'success': True})

    def update_harmonies(self, harmonies_id, comment):
        palette = ColorPalette.query.get(harmonies_id)
        palette.comment = comment
        self.color_harmonies_repository.update_harmonies(harmonies_id, comment)
        return jsonify({'success': True})

    def delete_harmonies(self, harmonies_id):
        color_harmonies = self.color_harmonies_repository.get_harmonies(harmonies_id)
        color_ids = color_harmonies.colors
        c1 = self.color_repository.get_color(color_ids[0].id)
        if not c1.displayable and (c1.color_palettes[0].id == harmonies_id and len(c1.color_palettes) == 1):
            self.color_repository.delete_color(c1, [])
        if len(color_ids) == 2:
            c2 = self.color_repository.get_color(color_ids[1].id)
            if not c2.displayable and (c2.color_palettes[0].id == harmonies_id and len(c2.color_palettes) == 1):
                self.color_repository.delete_color(c2, [])
        self.color_harmonies_repository.delete_harmonies(color_harmonies)
        return jsonify({'success': True})
