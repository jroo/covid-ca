from flask import render_template
from models import *


def average_daily_change_cases(q):
    # calculate average rate of change from day to day for past seven days
    x = 0
    for i in range(0, 7):
        new_cases = q[i].total_cases - q[i + 1].total_cases
        change_previous = new_cases / q[i].total_cases
        x += change_previous
    return (x / 7) * 100


def average_daily_change_deaths(q):
    # calculate average rate of change from day to day for past seven days
    x = 0
    for i in range(0, 7):
        new_deaths = q[i].deaths - q[i + 1].deaths
        change_previous = new_deaths / q[i].deaths
        x += change_previous
    return (x / 7) * 100


def ontario():
    # get daily numbers
    q = Daily.select().order_by(Daily.report_date.desc()).limit(8)
    pq = PT.get(name='Ontario')

    d = {}
    d['report_date'] = q[0].report_date
    d['new_cases'] = q[0].total_cases - q[1].total_cases
    d['total_cases'] = q[0].total_cases
    d['yesterday_total'] = q[1].total_cases
    d['change_previous'] = round(d['new_cases'] / q[0].total_cases * 100, 2)
    d['change_seven'] = round(average_daily_change_cases(q), 2)
    d['new_deaths'] = q[0].deaths - q[1].deaths
    d['total_deaths'] = q[0].deaths
    d['death_change_previous'] = round(d['new_deaths'] / q[0].deaths * 100, 2)
    d['yesterday_deaths'] = q[1].deaths
    d['death_change_seven'] = round(average_daily_change_deaths(q), 2)
    d['in_hospital'] = q[0].hospitalizations
    d['in_icu'] = q[0].icu
    d['on_ventilator'] = q[0].icu_ventilator
    d['hospital_beds'] = pq.hospital_beds
    d['icu_beds'] = pq.icu_beds
    d['ventilators'] = pq.ventilators

    return render_template("ontario.html", d=d)
