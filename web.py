from flask import Flask, render_template
from flask_caching import Cache
from models import *
from views.pt import *

import os


app = Flask(__name__)

CACHE_TYPE = 'null'
if (os.environ['FLASK_ENV'] == 'production'):
    CACHE_TYPE = 'redis'

cache = Cache(app, config={
    'CACHE_TYPE': CACHE_TYPE,
    'CACHE_DEFAULT_TIMEOUT': 3600,
    'CACHE_KEY_PREFIX': 'covid-ca-flask-',
    'CACHE_REDIS_URL': os.environ['REDIS_URL']
})


@app.route('/')
@cache.cached()
def index():
    return pt('Canada')


@app.route('/<pt_name>/')
@cache.cached()
def pt_report(pt_name):
    return pt(pt_name)


@app.route('/<pt_name>/daily.json')
@cache.cached()
def pt_report_json(pt_name):
    return pt_daily_json(pt_name)


@app.route('/ontario/cases.json')
@cache.cached()
def ontario_cases():
    query = Cases.select().where(Cases.province_territory == "Ontario")
    s = []
    for row in query:
        s.append(model_to_dict(row))
    return jsonify(s)


@app.route('/sources.html')
@cache.cached()
def sources():
    return render_template('sources.html', d=None)
