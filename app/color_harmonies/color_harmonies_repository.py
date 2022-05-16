from sqlalchemy import desc

from app import db
from app.models import ColorPalette


class ColorHarmoniesRepository:

    def __init__(self):
        pass

    def get_harmonies(self, harmonies_id):
        return ColorPalette.query.get(harmonies_id)

    def get_all_harmonies(self):
        return ColorPalette.query.order_by(desc(ColorPalette.date)).all()

    def add_harmonies(self, harmonies):
        db.session.add(harmonies)
        db.session.commit()

    def update_harmonies(self, harmonies_id, comment):
        color = ColorPalette.query.get(harmonies_id)
        color.comment = comment
        db.session.commit()

    def delete_harmonies(self, harmonies):
        db.session.delete(harmonies)
        db.session.commit()
