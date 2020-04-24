import os

from flask import Flask
from peewee import *
from playhouse.db_url import connect

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

db = connect(os.environ['DATABASE_URL'])


class BaseModel(Model):
    class Meta:
        database = db


class Daily(BaseModel):
    region = CharField()
    report_date = DateTimeField()
    confirmed_positive = IntegerField(null=True)
    resolved = IntegerField(null=True)
    deaths = IntegerField(null=True)
    TotalCases = IntegerField(null=True)
    TestsPastDay = IntegerField(null=True)
    UnderInvestigation = IntegerField(null=True)
    Hospitalizations = IntegerField(null=True)
    ICU = IntegerField(null=True)
    ICUVentilator = IntegerField(null=True)


db.create_tables([Daily])
