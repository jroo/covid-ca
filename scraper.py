from models import *

import csv
import os
import requests
import threading
import time

print ('Hello Ontario')
print ('Checking for changes to %s' % os.environ['ONTARIO_STATUS_URL'])


# check for update every 30 minutes
def check_data():
    print ("Checking %s" % time.ctime())
    threading.Timer(1800, check_data).start()
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

    print ("Processing row %s %s" % ('Ontario', row[0]))

    Daily.insert(
        region='Ontario',
        report_date=row[0],
        confirmed_positive=row[4],
        resolved=row[5],
        deaths=row[6],
        total_cases=row[7],
        tests_past_day=row[9],
        under_investigation=row[10],
        hospitalizations=row[11],
        icu=row[12],
        icu_ventilator=row[13]
    ).on_conflict_ignore().execute()
    

if __name__ == '__main__':
    check_data()
