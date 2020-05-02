from flask import Flask, render_template
from models import *
from reports.pt import pt, pt_daily_json

app = Flask(__name__)


@app.route('/')
def index():
    return pt('Canada')


@app.route('/<pt_name>/')
def pt_report(pt_name):
    return pt(pt_name)


@app.route('/<pt_name>/daily.json')
def pt_report_json(pt_name):
    return pt_daily_json(pt_name)


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
