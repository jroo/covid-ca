from models import *
from import_utils import fill_all_regions_past_days

import csv
import datetime
import os
import requests
import time


# create range of dates between start date and seven days before end date
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days) - 6):
        yield start_date + datetime.timedelta(n)


# check for update
def check_data():
    print ("Checking for updates: %s" % time.ctime())

    # get all regions
    pts = PT.select().order_by(PT.name)

    with requests.Session() as s:
        download = s.get(os.environ['PUBLIC_HEALTH_DAILY_URL'])
        decoded = download.content.decode('utf-8')
        cr = csv.reader(decoded.splitlines(), delimiter=',')
        cr_list = list(cr)

    print ("Process daily totals and create records for empty dates")
    # loop through each pt
    for pt in pts:
        pt_list = []
        for i in range(len(cr_list)):
            # create list of daily totals for just this PT
            if (i > 0):
                if (cr_list[i][1] == pt.name):
                    pt_list.append(cr_list[i])

        # loop through daily totals in list and process if PHAC approved or if
        # totals have changed since previous day
        for j in range(len(pt_list)):
            if (pt_list[j][12] != ''):
                # PHAC Approved
                process_row(pt_list[j])
            elif (pt_list[j][7] != pt_list[j - 1][7]):
                if (pt_list[j][1] != 'Canada'):
                    # Totals changed (all but Canada)
                    process_row(pt_list[j])

        # loop through each date between 1/31 and a week ago
        # and add an empty record if a record for that date doesn't exist
        start_date = datetime.date(2020, 1, 26)
        end_date = datetime.date.today()
        for single_date in daterange(start_date, end_date):
            Daily.get_or_create(
                report_date = single_date,
                region = pt)


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
    print ('\nCanada Daily')
    print ('-------------')
    print ('Checking for changes to %s' %
           os.environ['PUBLIC_HEALTH_DAILY_URL'])
    check_data()
    print ('Calculating past day totals')
    fill_all_regions_past_days()
    print ('Complete\n')
