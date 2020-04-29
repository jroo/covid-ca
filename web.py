from flask import jsonify, Flask, render_template
from models import *
from reports.pt import pt
from playhouse.shortcuts import model_to_dict

import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return ''


@app.route('/<pt_name>/')
def pt_report(pt_name):
    return pt(pt_name)


@app.route('/ontario/daily.json')
def ontario_daily():
    query = Daily.select().where(Daily.region == "Ontario")

    s = []
    for row in query:
        s.append(model_to_dict(row))

    return jsonify(s)


@app.route('/ontario/cases.json')
def ontario_cases():
    query = Cases.select().where(Cases.province_territory == "Ontario")

    s = []
    for row in query:
        s.append(model_to_dict(row))

    return jsonify(s)


@app.route('/sources.html')
def sources():
    return render_template('sources.html', d=None)
