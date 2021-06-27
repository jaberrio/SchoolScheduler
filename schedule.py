import json
from db import *

# assume that each class offering has the same id but can be multiple periods
def generate_schedule():
    #db.drop_schedules() # wipe schedule table
    idx = 1
    while idx <= 7:
        # get all schedules
        preferences = get_preferences_period(idx)
        for p in preferences:
            #preference = dict(p)
            # check if the course exists, and isn't full
            if course_available(p[0], p[1], p[2]):
                insert_schedule(p[0], p[1], idx)
            else:
                insert_schedule(0, p[1], idx)
        idx = idx + 1