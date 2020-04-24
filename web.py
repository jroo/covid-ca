from flask import Flask
from models import *
from peewee import *
from playhouse.db_url import connect

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'
