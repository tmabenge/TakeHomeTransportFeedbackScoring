import calendar
import datetime
import time


def get_weekday(date):
    # weekdays as a tuple
    week_days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    date_array = date.split('/')
    date_time = datetime.date(int(date_array[0]), int(date_array[1]), int(date_array[2]))
    day = date_time.weekday()

    return week_days[day]


def gm_time():
    """
    Returns timestamp

    :return: timestamp
    """
    gmt = time.gmtime()
    ts_calendar = calendar.timegm(gmt)
    return ts_calendar
