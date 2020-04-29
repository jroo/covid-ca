from models import *

import csv
import datetime
import os
import requests
import time

print ('Canada Daily')
print ('Checking for changes to %s' % os.environ['PUBLIC_HEALTH_DAILY_URL'])


# check for update
def check_data():
    print ("Checking for updates: %s" % time.ctime())
    with requests.Session() as s:
        download = s.get(os.environ['PUBLIC_HEALTH_DAILY_URL'])
        decoded = download.content.decode('utf-8')
        cr = csv.reader(decoded.splitlines(), delimiter=',')
        cr_list = list(cr)
        for i in range(len(cr_list)):
            # process all but header row
            if (i > 0):
                process_row(cr_list[i])


# for each day in a provinces data set,
# calculate and save number of new tests
def calc_daily_tests():
    print ('Calculating daily tests: %s' % time.ctime())
    pts = PT.select().order_by(PT.name)
    for pt in pts:
        pt_summaries = Daily.select().where(Daily.region == pt.name).order_by(
            Daily.report_date)
        for i in range(len(pt_summaries)):
            if (i > 0):
                if (not pt_summaries[i].tests_past_day):
                    if (pt_summaries[i].total_tests and pt_summaries[i - 1].total_tests):
                        tpd = int(pt_summaries[i].total_tests) - \
                            int(pt_summaries[i - 1].total_tests)
                        Daily.update(tests_past_day=tpd).where(
                            Daily.region == pt_summaries[i].region, Daily.report_date == pt_summaries[i].report_date).execute()


# process (clean and add) a row of data


def process_row(row):
    row[9] = row[9].replace('N/A', '').strip()

    # convert blanks to null
    for i in range(len(row)):
        if row[i] == '':
            row[i] = None

    timeArr = row[3].split('-')
    rd = datetime.datetime(int(timeArr[2]), int(timeArr[1]), int(timeArr[0]))

    Daily.insert(
        region=row[1],
        report_date=rd,
        confirmed_positive=None,
        deaths=row[6],
        total_cases=row[7],
        total_tests=row[8],
        resolved=row[9],
        tests_past_day=None,
        cases_past_day=row[12],
        under_investigation=None,
        hospitalizations=None,
        icu=None,
        icu_ventilator=None
    ).on_conflict_ignore().execute()


if __name__ == '__main__':
    check_data()
    calc_daily_tests()
