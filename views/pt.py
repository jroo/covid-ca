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


def rolling_average(q, i, field):
    # calculate 7 day rolling average for field
    x = 0
    rolling_total = 0
    rolling_average = None
    if i > 5:
        for j in range(0, 7):
            if (getattr(q[i-j], field)):
                rolling_total += getattr(q[i-j], field)

        rolling_average = weird_division(rolling_total, 7)
    return rolling_average


# given a metric, find the number of days it took to double to current value
def double_rate(metric, pt_name, latest_row):
    if (getattr(latest_row, metric)) > 1:
        half_row = Daily.select().where(
            getattr(Daily, metric) < getattr(latest_row, metric) / 2).where(
            fn.Lower(Daily.region) == pt_name.lower()).order_by(
            Daily.report_date.desc()).limit(1)
        difference = latest_row.report_date - half_row[0].report_date
        difference_days = difference.days
    else:
        difference_days = None
    return difference_days


# return zero if dividing by zero
def weird_division(n, d):
    return n / d if d else 0

# package up data for template


def package_up(pt_name, q, pq):
    d = {}

    if (q and pq):
        #  info
        d['region'] = q[0].region
        d['region_path'] = '/%s/' % pt_name.replace(' ', '-')
        d['report_date'] = q[0].report_date

        # cases
        d['new_cases'] = q[0].total_cases - q[1].total_cases
        d['total_cases'] = q[0].total_cases
        d['yesterday_total'] = q[1].total_cases
        d['change_previous'] = round(weird_division(
            d['new_cases'], q[1].total_cases) * 100, 1)
        d['change_seven'] = round(average_daily_change_cases(q), 2)
        d['case_double_rate'] = double_rate('total_cases', pt_name, q[0])

        # death info
        d['new_deaths'] = q[0].deaths - q[1].deaths
        d['total_deaths'] = q[0].deaths
        d['death_change_previous'] = round(
            weird_division(d['new_deaths'], q[1].deaths) * 100, 1)
        d['yesterday_deaths'] = q[1].deaths
        d['death_change_seven'] = round(average_daily_change_deaths(q), 2)
        d['death_double_rate'] = double_rate('deaths', pt_name, q[0])

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
        d['display_cases'] = (d['total_cases'] is not None and
                              d['yesterday_total'] is not None)
        d['display_deaths'] = (d['total_deaths'] is not None and
                               d['yesterday_deaths'] is not None)
        d['display_hospital'] = (d['in_hospital'] is not None and
                                 d['in_icu'] is not None)
        d['display_testing'] = (d['total_tests'] is not None and
                                d['daily_tests_per_100k'] is not None)
        d['display_testing_goals'] = (pt_name == 'Ontario')

    return d


def pt(pt_name):
    # get daily numbers

    try:
        q = Daily.select().where(
            fn.Lower(Daily.region) == pt_name).order_by(
            Daily.report_date.desc()).limit(8)
        pq = PT.get(fn.Lower(PT.name) == pt_name)
    except DoesNotExist:
        abort(404)

    d = package_up(pt_name, q, pq)

    return render_template("pt.html", d=d)


def pt_daily_json(pt_name):
    try:
        q = Daily.select().where(
            fn.Lower(Daily.region) == pt_name).where(
            Daily.report_date > '2020-02-28').order_by(
            Daily.report_date);
        pq = PT.get(fn.Lower(PT.name) == pt_name)
    except:
        abort(404)

    s = []
    for i, row in enumerate(q):
        d_row = model_to_dict(row)

        # add tests_past_day_per_100k
        d_row['tests_past_day_per_100k'] = round(
            row.tests_past_day / (pq.population / 100000), 1) if row.tests_past_day else None   
        d_row['cases_past_day_rolling_average'] = rolling_average(q, i, 'cases_past_day')
        d_row['deaths_past_day_rolling_average'] = rolling_average(q, i, 'deaths_past_day')
        tests_past_day_rolling_average = rolling_average(q, i, 'tests_past_day')
        d_row['tests_past_day_per_100k_rolling_average'] = round(
                tests_past_day_rolling_average / (pq.population / 100000), 1) if tests_past_day_rolling_average else None
        s.append(d_row)

    return jsonify(s)


def pt_chart(pt_name):
    return render_template("chart.html")


def sources():
    source_list = []
    script_path = os.path.dirname(__file__)
    relative_path = '../data/regions.json'
    with open(os.path.join(script_path, relative_path)) as f:
        data = json.load(f)
        for pt in data:
            if len(pt['sources']) > 0:
                source_list.append(pt)

    return render_template('sources.html', source_list=source_list)
