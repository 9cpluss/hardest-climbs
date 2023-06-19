from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Climbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))


class Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer)
    french = db.Column(db.String(15))
    us = db.Column(db.String(15))
    style = db.Column(db.String(31))


class Climbs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    style = db.Column(db.String(31))
    fa_id = db.Column(db.Integer, db.ForeignKey("climbers.id"), nullable=False)
    fa_date = db.Column(db.String(15))
    grade_id = db.Column(db.Integer, db.ForeignKey("grades.id"), nullable=False)
    country = db.Column(db.String(255))
    area = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)


class Repeats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    climb_id = db.Column(db.Integer, db.ForeignKey("climbs.id"), nullable=False)
    climber_id = db.Column(db.Integer, db.ForeignKey("climbers.id"), nullable=False)


class Videos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    climb_id = db.Column(db.Integer, db.ForeignKey("climbs.id"), nullable=False)
    climber_id = db.Column(db.Integer, db.ForeignKey("climbers.id"), nullable=False)
    url = db.Column(db.String(255))
