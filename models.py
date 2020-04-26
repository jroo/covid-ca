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


db.create_tables([Daily, Cases])
