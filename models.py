import os
from peewee import *
from playhouse.db_url import connect

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
    total_cases = IntegerField(null=True)
    tests_past_day = IntegerField(null=True)
    under_investigation = IntegerField(null=True)
    hospitalizations = IntegerField(null=True)
    icu = IntegerField(null=True)
    icu_ventilator = IntegerField(null=True)

    class Meta:
        primary_key = CompositeKey('region', 'report_date')


db.create_tables([Daily])
