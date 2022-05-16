from sqlalchemy import desc

from app import db
from app.models import Color


class ColorRepository:

    def __init__(self):
        pass

    def get_color(self, color_id):
        return Color.query.get(color_id)

    def get_colors(self):
        return Color.query.order_by(desc(Color.date)).all()

    def get_color_descending_id(self):
        return Color.query.order_by(-Color.id)

    def add_color(self, color):
        db.session.add(color)
        db.session.commit()

    def update_color(self, color_id, comment):
        # raise Exception('general exceptions not caught by specific handling')
        color = Color.query.get(color_id)
        color.comment = comment
        db.session.commit()

    def delete_color(self, color, color_harmonies_ids):
        if len(color_harmonies_ids) == 0:
            db.session.delete(Color.query.get(color.id))
            db.session.commit()
        else:
            color.displayable = False
            db.session.commit()
