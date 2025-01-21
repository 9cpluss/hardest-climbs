import os
import json
import git
import pandas as pd

from flask import render_template
from flask import Flask, request
from http import HTTPStatus

from src.auth import signature_verified
from src.update import update
from src.utils import json_to_dataframe, create_climber_key, split_name


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


app = Flask("Hardest Climbs", template_folder=THIS_FOLDER + "/templates")

with open(os.path.join(THIS_FOLDER, 'data/lead.json'), "r", encoding='utf-8') as f:
    lead_data = json.load(f)

with open(os.path.join(THIS_FOLDER, 'data/boulder.json'), "r", encoding='utf-8') as f:
    boulder_data = json.load(f)


lead = json_to_dataframe(json_data=lead_data)
boulder = json_to_dataframe(json_data=boulder_data)
data = pd.concat([lead, boulder])
data = data.sort_values(
    by=["style", "rank", "name", "last_name"],
    ascending=False,
)


@app.route('/')
def index():
    grades = request.args.get("grades", default="fr")

    unique_climbs = data[data["is_fa"]]

    climbs = pd.concat([
        unique_climbs[unique_climbs["style"] == "sport"][0:1],
        unique_climbs[unique_climbs["style"] == "bouldering"][0:1],
        unique_climbs[unique_climbs["style"] == "sport"][1:2],
        unique_climbs[unique_climbs["style"] == "bouldering"][1:2],
        unique_climbs[unique_climbs["style"] == "sport"][2:3],
        unique_climbs[unique_climbs["style"] == "bouldering"][2:3],
    ])

    return render_template('index.html', climbs=climbs, grades=grades)


@app.route('/sport')
def sport():
    grades = request.args.get("grades", default="fr")
    climbs = data[(data["is_fa"]) & (data["style"] == "sport")]

    return render_template(
        'generic.html',
        title="Sport Climbing",
        category="sport",
        climbs=climbs,
        grades=grades,
    )


@app.route("/bouldering")
def bouldering():
    grades = request.args.get("grades", default="fr")
    climbs = data[(data["is_fa"]) & (data["style"] == "bouldering")]

    return render_template(
        'generic.html',
        title="Bouldering",
        category="bouldering",
        climbs=climbs,
        grades=grades,
    )


@app.route("/sport/climber/<climber>")
def sport_climber(climber):
    grades = request.args.get("grades", default="fr")
    climbs = data[(data["climber_key"] == climber) & (data["style"] == "sport")]

    if climbs.shape[0] > 0:
        return render_template(
            'generic.html',
            title=f"Sport Climbing: {climber.replace('+', ' ').title()}",
            category="sport",
            climbs=climbs,
            grades=grades,
        )
    else:
        return "Climber not found", 404
    

@app.route("/sport/route/<route>")
def sport_route(route):
    grades = request.args.get("grades", default="fr")
    climbs = data[(data["route_key"] == route) & (data["style"] == "sport") & (data["is_fa"])]

    if climbs.shape[0] > 0:
        return render_template(
            'generic.html',
            title="",
            category="sport",
            climbs=climbs,
            grades=grades,
        )
    else:
        return "Route not found", 404


@app.route("/bouldering/climber/<climber>")
def bouldering_climber(climber):
    grades = request.args.get("grades", default="fr")
    climbs = data[(data["climber_key"] == climber) & (data["style"] == "bouldering")]

    if climbs.shape[0] > 0:
        return render_template(
            'generic.html',
            title=f"Bouldering: {climber.replace('+', ' ').title()}",
            category="bouldering",
            climbs=climbs,
            grades=grades,
        )
    else:
        return "Climber not found", 404
    

@app.route("/bouldering/problem/<problem>")
def bouldering_problem(problem):
    grades = request.args.get("grades", default="fr")
    climbs = data[(data["route_key"] == problem) & (data["style"] == "bouldering") & (data["is_fa"])]

    if climbs.shape[0] > 0:
        return render_template(
            'generic.html',
            title="",
            category="bouldering",
            climbs=climbs,
            grades=grades,
        )
    else:
        return "Boulder not found", 404


@app.route("/update", methods=["POST"])
def webhook():
    if request.method != "POST":
        return 'Wrong event type', HTTPStatus.BAD_REQUEST

    # Get signature from headers
    signature_header = request.headers.get('X-Hub-Signature-256')
    if not signature_header:
        return 'No signature header', HTTPStatus.FORBIDDEN
    
    webhook_secret = os.environ.get('WEBHOOK_SECRET')
    if not webhook_secret:
        return 'Webhook secret not configured', HTTPStatus.INTERNAL_SERVER_ERROR

    if not signature_verified(request.data, webhook_secret, signature_header):
        return "Signature not verified", HTTPStatus.FORBIDDEN

    payload = request.get_json()
    
    if payload and payload.get("ref") == "refs/heads/master":
        try:
            repo = git.Repo("~/mysite")
            origin = repo.remotes.origin
            origin.pull()

            update()

            return 'Updated PythonAnywhere successfully', HTTPStatus.OK
        except Exception as e:
            return f'Error during update: {str(e)}', HTTPStatus.INTERNAL_SERVER_ERROR
        
    return "OK", HTTPStatus.OK


# helper template filters ----

@app.template_filter('bg_alternate')
def bg_alternate(index):
    return "secondary" if index % 2 == 0 else "dark"


@app.template_filter('climber_first_name')
def climber_first_name(name):
    return split_name(name)[0]


@app.template_filter('climber_last_name')
def climber_last_name(name):
    return split_name(name)[1]


@app.template_filter('climber_key')
def climber_key(name):
    return create_climber_key(name)