from flask import render_template
from models import *


def average_daily_change_cases(q):
    # calculate average rate of change from day to day for past seven days
    x = 0
    for i in range(0, 7):
        new_cases = q[i].total_cases - q[i + 1].total_cases
        change_previous = new_cases / q[i + 1].total_cases
        x += change_previous
    return (x / 7) * 100


def average_daily_change_deaths(q):
    # calculate average rate of change from day to day for past seven days
    x = 0
    for i in range(0, 7):
        new_deaths = q[i].deaths - q[i + 1].deaths
        change_previous = new_deaths / q[i + 1].deaths
        x += change_previous
    return (x / 7) * 100


def ontario():
    # get daily numbers
    q = Daily.select().order_by(Daily.report_date.desc()).limit(8)
    pq = PT.get(name='Ontario')

    d = {}
    d['report_date'] = q[0].report_date
    new_cases = q[0].total_cases - q[1].total_cases
    d['new_cases'] = f'{new_cases:,}'
    d['total_cases'] = q[0].total_cases
    d['yesterday_total'] = f'{q[1].total_cases:,}'
    d['change_previous'] = round(new_cases / q[1].total_cases * 100, 1)
    d['change_seven'] = round(average_daily_change_cases(q), 2)
    new_deaths = q[0].deaths - q[1].deaths
    d['new_deaths'] = f'{new_deaths:,}'
    d['total_deaths'] = f'{q[0].deaths:,}'
    d['death_change_previous'] = round(new_deaths / q[1].deaths * 100, 1)
    d['yesterday_deaths'] = f'{q[1].deaths:,}'
    d['death_change_seven'] = round(average_daily_change_deaths(q), 2)
    d['in_hospital'] = q[0].hospitalizations
    d['in_icu'] = f'{q[0].icu:,}'
    d['on_ventilator'] = f'{q[0].icu_ventilator:,}'
    d['hospital_beds'] = f'{pq.hospital_beds:,}'
    d['icu_beds'] = f'{pq.icu_beds:,}'
    d['ventilators'] = f'{pq.ventilators:,}'
    daily_tests = q[0].tests_past_day
    d['daily_tests'] = f'{daily_tests:,}'
    d['total_tests'] = f'{q[0].total_tests:,}'
    d['daily_tests_per_100k'] = round(
        daily_tests / (pq.population / 100000), 1)

    return render_template("ontario.html", d=d)
