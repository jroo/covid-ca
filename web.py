from flask import jsonify, Flask
from models import *
from reports.ontario import ontario
from playhouse.shortcuts import model_to_dict


app = Flask(__name__)


@app.route('/')
def hello_world():
    return ''


@app.route('/ontario/')
def ontario_report():
    return ontario()


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
