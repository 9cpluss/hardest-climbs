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
