import datetime
import logging

import dateparser

DATE_FORMAT = '%d.%m.%Y %H:%M%p'

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
