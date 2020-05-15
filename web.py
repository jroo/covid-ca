from datetime import date
from flask import Flask, redirect, render_template
from flask.json import JSONEncoder
from flask_caching import Cache
from models import *
from views.pt import *

import os

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

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
    return redirect('/canada/')


@app.route('/<pt_name>/')
@cache.cached()
def pt_report(pt_name):
    pt_name = pt_name.lower().replace('-', ' ')
    return pt(pt_name)


@app.route('/<pt_name>/daily.json')
@cache.cached()
def pt_report_json(pt_name):
    pt_name = pt_name.lower().replace('-', ' ')
    return pt_daily_json(pt_name)


@app.route('/<pt_name>/chart')
@cache.cached()
def pt_report_chart(pt_name):
    return pt_chart(pt_name)


@app.route('/ontario/cases.json')
@cache.cached()
def ontario_cases():
    query = Cases.select().where(Cases.province_territory == "Ontario")
    s = []
    for row in query:
        s.append(model_to_dict(row))
    return jsonify(s)


@app.route('/sources/')
@cache.cached()
def pt_sources():
    return sources()

@app.route('/about/')
@cache.cached()
def about():
    return render_template("about.html")
