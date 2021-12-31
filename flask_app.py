import os
import json
from flask import render_template
from flask import Flask

from functions import create_html_columns, create_html_from_json_element

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


app = Flask("Hardest Climbs", template_folder='/home/9cpluss/mysite')

with open(os.path.join(THIS_FOLDER, 'data/lead.json'), "r") as f:
    lead_data = json.load(f)

with open(os.path.join(THIS_FOLDER, 'data/boulder.json'), "r") as f:
    boulder_data = json.load(f)


@app.route('/')
def index():
    climbs = []
    for i, (l, b) in enumerate(zip(lead_data[0:3], boulder_data[0:3])):
        if i % 2 == 0:
            climbs.append(create_html_from_json_element(l))
            climbs.append(create_html_from_json_element(b))
        else:
            climbs.append(create_html_from_json_element(l, bg="dark"))
            climbs.append(create_html_from_json_element(b, bg="dark"))


    return render_template('index.html', climbs="".join(climbs))

@app.route('/sport')
def sport():
    climbs = create_html_columns(lead_data)

    # TODO Fix template
    return render_template('generic.html', title="Sport Climbing", climbs=climbs)

@app.route("/bouldering")
def bouldering():
    climbs = create_html_columns(boulder_data)

    # TODO Fix template
    return render_template('generic.html', title="Bouldering", climbs=climbs)
