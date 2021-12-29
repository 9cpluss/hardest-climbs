import json
from flask import render_template
from flask import Flask

app = Flask("9c plus", template_folder='/home/9cpluss/hardest-climbs')


with open("data.json", "r") as f:
    data = json.load(f)


@app.route('/')
def index():
    return render_template('index.html')
