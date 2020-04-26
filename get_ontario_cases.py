from models import *

import csv
import os
import requests
import time

print ('Ontario Cases')
print ('Checking for changes to %s' % os.environ['ONTARIO_STATUS_URL'])


# check for update
def check_data():
    print ("Checking %s" % time.ctime())
    with requests.Session() as s:
        download = s.get(os.environ['ONTARIO_CONFIRMED_POSITIVE_URL'])
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

    Cases.insert(
        province_territory='Ontario',
        source_id=row[0],
        episode_date=row[1],
        age_group=row[2],
        gender=row[3],
        how_contracted=row[4],
        outcome=row[5],
        health_unit=row[6],
        health_unit_address=row[7],
        health_unit_city=row[8],
        health_unit_postal_code=row[9],
        health_unit_latitude=row[11],
        health_unit_longitude=row[12]
    ).on_conflict_ignore().execute()


if __name__ == '__main__':
    check_data()
