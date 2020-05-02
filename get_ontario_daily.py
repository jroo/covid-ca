from models import *
from import_utils import fill_past_days

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


if __name__ == '__main__':
    print ('\nOntario Daily')
    print ('-------------')
    print ('Checking for changes to %s' % os.environ['ONTARIO_STATUS_URL'])
    check_data()
    fill_past_days('Ontario')
    print ("Complete\n")
