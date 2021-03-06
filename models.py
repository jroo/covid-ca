import json
import os
from peewee import *
from playhouse.db_url import connect

db = connect(os.environ['DATABASE_URL'])


class BaseModel(Model):
    class Meta:
        database = db


class PT(BaseModel):
    name = CharField(primary_key=True)
    nom = CharField()
    abbreviation = CharField()
    url = CharField(null=True)
    population = IntegerField()
    hospital_beds = IntegerField(null=True)
    icu_beds = IntegerField(null=True)
    ventilators = IntegerField(null=True)
    daily_data_url = CharField(null=True)


class Daily(BaseModel):
    region = CharField()
    report_date = DateTimeField()
    confirmed_positive = IntegerField(null=True)
    resolved = IntegerField(null=True)
    deaths = IntegerField(null=True)
    total_cases = IntegerField(null=True)
    cases_past_day = IntegerField(null=True)
    deaths_past_day = IntegerField(null=True)
    tests_past_day = IntegerField(null=True)
    total_tests = IntegerField(null=True)
    under_investigation = IntegerField(null=True)
    hospitalizations = IntegerField(null=True)
    icu = IntegerField(null=True)
    icu_ventilator = IntegerField(null=True)

    class Meta:
        primary_key = CompositeKey('region', 'report_date')


class Cases(BaseModel):
    province_territory = CharField()
    source_id = IntegerField()
    episode_date = DateTimeField(null=True)
    age_group = CharField(null=True)
    gender = CharField(null=True)
    how_contracted = CharField(null=True)
    outcome = CharField(null=True)
    health_unit = CharField(null=True)
    health_unit_address = CharField(null=True)
    health_unit_city = CharField(null=True)
    health_unit_postal_code = CharField(null=True)
    health_unit_latitude = CharField(null=True)
    health_unit_longitude = CharField(null=True)

    class Meta:
        primary_key = CompositeKey('province_territory', 'source_id')


# initialize db
db.create_tables([PT, Daily, Cases])


# populate provinces and territories
script_path = os.path.dirname(__file__)
relative_path = 'data/regions.json'
with open(os.path.join(script_path, relative_path)) as f:
    data = json.load(f)
    for pt in data:
        PT.insert(
            name=pt['name'],
            nom=pt['nom'],
            abbreviation=pt['abbreviation'],
            url=pt['url'],
            population=pt['population'],
            hospital_beds=pt['hospital_beds'],
            icu_beds=pt['icu_beds'],
            ventilators=pt['ventilators'],
            daily_data_url=pt['daily_data_url']
        ).on_conflict_ignore().execute()
