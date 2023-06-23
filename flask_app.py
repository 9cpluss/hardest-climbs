import os
import json
import git

from flask import render_template
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy.orm import aliased

from src.update import update
from src.tunnel import create_tunnel
from src.config import settings
from src.models import db, Climbers, Climbs, Repeats, Videos, Grades


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

app = Flask("Hardest Climbs", template_folder=THIS_FOLDER + "/templates")


# Database
if settings.local:
    tunnel = create_tunnel()
    tunnel.start()

    db_uri = "mysql://{user}:{pwd}@127.0.0.1:{port}/{user}${schema}".format(
        user=settings.db_username,
        pwd=settings.db_password,
        port=tunnel.local_bind_port,
        schema=settings.db_schema,
    )
else:
    db_uri = "mysql://{user}:{pwd}@127.0.0.1/{user}${schema}".format(
        user=settings.db_username,
        pwd=settings.db_password,
        schema=settings.db_schema,
    )


app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config['SQLALCHEMY_ECHO'] = True  # TODO: Remove after development

db.init_app(app)


@app.route('/')
def index():
    # TODO: All info
    select_lead = db.select(Climbs, Grades, Climbers).\
        join(Grades).join(Climbers).\
        where(and_(Climbs.style == "sport", Grades.rank >= 3)).\
        order_by(Grades.rank.desc(), Climbs.name.asc()).\
        limit(3)
    select_boulder = db.select(Climbs, Grades, Climbers).\
        join(Grades).join(Climbers).\
        where(and_(Climbs.style == "bouldering", Grades.rank >= 3)).\
        order_by(Grades.rank.desc(), Climbs.name.asc()).\
        limit(3)

    lead = db.session.execute(select_lead).all()
    boulder = db.session.execute(select_boulder).all()

    # Mix them together
    climbs = [item for sublist in zip(lead, boulder) for item in sublist]

    return render_template('index.html', climbs=climbs)


@app.route('/sport')
def sport():
    # TODO: Climbs are duplicated now (how to handle repeats)
    RepeatClimbers = aliased(Climbers)
    select = db.select(Climbs, Grades, Climbers, RepeatClimbers).\
        join(Grades).join(Climbers).join(Repeats, Climbs.id == Repeats.climb_id, isouter=True).join(RepeatClimbers, isouter=True).\
        where(Climbs.style == "sport").\
        order_by(Grades.rank.desc(), Climbs.name.asc())
    
    climbs = db.session.execute(select)
        
    return render_template('generic.html', title="Sport Climbing", category="sport", climbs=climbs)


@app.route('/sport/<route_id>')
def sport_route(route_id):
    # TODO: WIP needs proper implementation
    RepeatClimbers = aliased(Climbers)
    select = db.select(Climbs, Grades, Climbers, RepeatClimbers).\
        join(Grades).join(Climbers).join(Repeats, Climbs.id == Repeats.climb_id, isouter=True).join(RepeatClimbers, isouter=True).\
        where(and_(Climbs.style == "sport", Climbs.id == route_id))
    
    climbs = db.session.execute(select)
        
    return render_template('generic.html', category="sport", climbs=climbs)


# @app.route("/bouldering")
# def bouldering():
#     return render_template('generic.html', title="Bouldering", category="bouldering", climbs=boulder_data)


# @app.route("/sport/<climber>")
# def sport_climber(climber):
#     return render_template('generic.html', title=f"Sport Climbing: {climber.capitalize()}", category="sport", climbs=climber_ascents(climber, lead_data))


# @app.route("/bouldering/<climber>")
# def bouldering_climber(climber):
#     return render_template('generic.html', title=f"Bouldering: {climber.capitalize()}", category="bouldering", climbs=climber_ascents(climber, boulder_data))


@app.route("/update", methods=["POST"])
def webhook():
    if request.method == "POST":
        repo = git.Repo("~/mysite")
        origin = repo.remotes.origin
        origin.pull()
        
        update()
        
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
