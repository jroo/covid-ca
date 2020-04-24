from flask import jsonify, Flask, Response
from models import *
from playhouse.shortcuts import model_to_dict


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/ontario.json')
def ontario():
    query = Daily.select().where(Daily.region == "Ontario")

    s = []
    for row in query:
        s.append(model_to_dict(row))

    return jsonify(s)
