from models import *

import csv
import os
import requests
import time


# check for update
def check_data():
    print ("Checking for updates: %s" % time.ctime())
    with requests.Session() as s:
        download = s.get(os.environ['ONTARIO_STATUS_URL'])
        decoded = download.content.decode('utf-8')
        cr = csv.reader(decoded.splitlines(), delimiter=',')
        cr_list = list(cr)
        for i in range(len(cr_list)):
            if (i > 0):
                process_row(cr_list[i])


# process (add or update) a row of data
def process_row(row):

    # convert blanks to null
    for i in range(len(row)):
        if row[i] == '':
            row[i] = None

    Daily.insert(
        region='Ontario',
        report_date=row[0],
        confirmed_positive=row[4],
        resolved=row[5],
        deaths=row[6],
        total_cases=row[7],
        total_tests=row[8],
        tests_past_day=row[9],
        under_investigation=row[10],
        hospitalizations=row[11],
        icu=row[12],
        icu_ventilator=row[13]
    ).on_conflict_ignore().execute()


# if past day totals are null, calculate and save them
def fill_past_days():
    q = Daily.select().where(
        Daily.region == 'Ontario').order_by(
        Daily.report_date.desc())

    for i in range(0, len(q)):
        print ('\n')
        print (q[i])
        if (i < len(q) - 1):
            if not q[i].tests_past_day:
                print ("calulating tests past day")
                try:
                    q[i].tests_past_day = q[i].total_tests - q[i + 1].total_tests
                    q[i].save()
                except TypeError:
                    pass
            if not q[i].cases_past_day:
                print ("calulating cases past day")
                try:
                    q[i].cases_past_day = q[i].total_cases - q[i + 1].total_cases
                    q[i].save()
                except TypeError:
                    pass
            if not q[i].deaths_past_day:
                print ("calulating deaths past day")
                try:
                    q[i].deaths_past_day = q[i].deaths - q[i + 1].deaths
                    q[i].save()
                except TypeError:
                    pass

if __name__ == '__main__':
    print ('\nOntario Daily')
    print ('-------------')
    print ('Checking for changes to %s' % os.environ['ONTARIO_STATUS_URL'])
    check_data()
    fill_past_days()
    print ("Complete\n")
