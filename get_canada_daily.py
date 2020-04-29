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
            # process all but header row
            if (i > 0):
                process_row(cr_list[i])


# process (clean and add) a row of data
def process_row(row):
    print ("Processing row %s %s" % ('Canada', row))
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
        under_investigation=None,
        hospitalizations=None,
        icu=None,
        icu_ventilator=None
    ).on_conflict_ignore().execute()


if __name__ == '__main__':
    check_data()
