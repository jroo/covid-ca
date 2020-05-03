from flask import abort, jsonify, render_template
from models import *
from playhouse.shortcuts import model_to_dict


def average_daily_change_cases(q):
    # calculate average rate of change from day to day for past seven days
    x = 0
    for i in range(0, 7):
        new_cases = q[i].total_cases - q[i + 1].total_cases
        change_previous = weird_division(new_cases, q[i + 1].total_cases)
        x += change_previous
    return (x / 7) * 100


def average_daily_change_deaths(q):
    # calculate average rate of change from day to day for past seven days
    x = 0
    for i in range(0, 7):
        new_deaths = q[i].deaths - q[i + 1].deaths
        change_previous = weird_division(new_deaths, q[i + 1].deaths)
        x += change_previous
    return (x / 7) * 100


# return zero if dividing by zero
def weird_division(n, d):
    return n / d if d else 0

# package up data for template


def package_up(pt_name, q, pq):
    d = {}

    if (q and pq):
        #  info
        d['region'] = q[0].region
        d['report_date'] = q[0].report_date
        d['new_cases'] = q[0].total_cases - q[1].total_cases
        d['total_cases'] = q[0].total_cases
        d['yesterday_total'] = q[1].total_cases
        d['change_previous'] = round(weird_division(
            d['new_cases'], q[1].total_cases) * 100, 1)
        d['change_seven'] = round(average_daily_change_cases(q), 2)

        # death info
        d['new_deaths'] = q[0].deaths - q[1].deaths
        d['total_deaths'] = q[0].deaths
        d['death_change_previous'] = round(
            weird_division(d['new_deaths'], q[1].deaths) * 100, 1)
        d['yesterday_deaths'] = q[1].deaths
        d['death_change_seven'] = round(average_daily_change_deaths(q), 2)

        # hospital info
        d['in_hospital'] = q[0].hospitalizations
        d['in_icu'] = q[0].icu
        d['on_ventilator'] = q[0].icu_ventilator
        d['hospital_beds'] = pq.hospital_beds
        d['icu_beds'] = pq.icu_beds
        d['ventilators'] = pq.ventilators

        # testing info
        d['daily_tests'] = q[0].tests_past_day
        d['total_tests'] = q[0].total_tests
        d['daily_tests_per_100k'] = round(
            d['daily_tests'] / (pq.population / 100000), 1)

        # display section flags
        d['display_cases'] = (d['new_cases'] and
                              d['total_cases'] and
                              d['yesterday_total'] and
                              d['change_previous'] and
                              d['change_seven'])
        d['display_deaths'] = (d['new_deaths'] and
                               d['total_deaths'] and
                               d['death_change_previous'] and
                               d['yesterday_deaths'] and
                               d['death_change_seven'])
        d['display_hospital'] = (d['in_hospital'] and d['in_icu'])
        d['display_testing'] = (
            d['daily_tests'] and
            d['total_tests'] and
            d['daily_tests_per_100k'])
        d['display_testing_goals'] = (pt_name == 'Ontario')

    return d


def pt(pt_name):
    # get daily numbers

    try:
        q = Daily.select().where(
            fn.Lower(Daily.region) == pt_name.lower()).order_by(
            Daily.report_date.desc()).limit(8)
        pq = PT.get(fn.Lower(PT.name) == pt_name.lower())
    except DoesNotExist:
        abort(404)

    d = package_up(pt_name, q, pq)

    return render_template("pt.html", d=d)


def pt_daily_json(pt_name):
    query = Daily.select().where(
        fn.Lower(Daily.region) == pt_name.lower()).order_by(
        Daily.report_date)

    s = []
    for row in query:
        s.append(model_to_dict(row))

    return jsonify(s)