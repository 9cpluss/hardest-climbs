from flask_app import db, app

with app.app_context():
    db.create_all()
