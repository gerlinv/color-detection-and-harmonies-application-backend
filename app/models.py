from app import db

color_groups = db.Table(
    "color_groups",
    db.Column("color_id", db.Integer, db.ForeignKey("color.id")),
    db.Column("color_palette_id", db.Integer, db.ForeignKey("color_palette.id")),
    db.PrimaryKeyConstraint("color_id", "color_palette_id")
)


class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    hue = db.Column(db.String(10))
    hex_code = db.Column(db.String(6))
    date = db.Column(db.DateTime)
    displayable = db.Column(db.Boolean, default=True)
    comment = db.Column(db.String(150))
    color_palettes = db.relationship("ColorPalette", secondary=color_groups, back_populates="colors")


class ColorPalette(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    analogous_harmony = db.Column(db.SmallInteger())
    complimentary_harmony = db.Column(db.SmallInteger())
    monochromatic_harmony = db.Column(db.SmallInteger())
    neutral_color_harmony = db.Column(db.SmallInteger())
    date = db.Column(db.DateTime)
    comment = db.Column(db.String(150))
    colors = db.relationship("Color", secondary=color_groups, back_populates="color_palettes")


db.create_all()
