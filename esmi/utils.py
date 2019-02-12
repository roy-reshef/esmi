import datetime
import logging

import dateparser

DATE_FORMAT = '%d.%m.%Y %H:%M%p'

WEEK_DAYS = {
    'sundays': 0,
    'mondays': 1,
    'tuesdays': 2,
    'wednesdays': 3,
    'thursdays': 4,
    'fridays': 5,
    'saturdays': 6,
    'sunday': 0,
    'monday': 1,
    'tuesday': 2,
    'wednesday': 3,
    'thursday': 4,
    'friday': 5,
    'saturday': 6,
}
WEEK_DAYS_REVERSE = dict(zip(WEEK_DAYS.values(), WEEK_DAYS.keys()))


logger = logging.getLogger()


def parse_date(date: str) -> datetime.datetime:
    if date is None:
        return None

    try:
        date: datetime = datetime.datetime.strptime(date, DATE_FORMAT)
    except ValueError:
        date: datetime = dateparser.parse(date)
    logger.debug("parsed date:{}".format(date))
    return date


def next_weekday(timestamp, weekday):
    days_ahead = day_str_to_int(weekday) - timestamp.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return timestamp + datetime.timedelta(days_ahead)


def day_str_to_int(day):
    return WEEK_DAYS[day]
