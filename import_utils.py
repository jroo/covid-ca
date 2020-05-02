from models import *

# if past day totals are null, calculate and save them for a region
def fill_past_days(region_name):
    q = Daily.select().where(
        Daily.region == region_name).order_by(
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


# go through every region and calculate past day totals
def fill_all_regions_past_days():
        # get all regions
        pts = PT.select().order_by(PT.name)

        # loop through them and update totals
        for pt in pts:
            fill_past_days(pt.name)
