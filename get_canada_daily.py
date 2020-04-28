from models import *

import csv
import datetime
import os
import requests
import time

print ('Canada Daily')
print ('Checking for changes to %s' % os.environ['BC_DAILY_URL'])


# check for update
def check_data():
    print ("Checking %s" % time.ctime())
    with requests.Session() as s:
        download = s.get(os.environ['PUBLIC_HEALTH_DAILY_URL'])
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

    print ("Processing row %s %s" % ('Canada', row[0]))
    print (row)

    timeArr = row[3].split('-')
    rd = datetime.datetime(int(timeArr[2]), int(timeArr[1]), int(timeArr[0]))

    Daily.insert(
        region=row[1],
        report_date=rd,
        confirmed_positive=None,
        deaths=row[6],
        total_cases=row[7],
        total_tests=row[8],
        tests_past_day=None,
        under_investigation=None,
        hospitalizations=None,
        icu=row[12],
        icu_ventilator=None
    ).on_conflict_ignore().execute()


if __name__ == '__main__':
    check_data()
