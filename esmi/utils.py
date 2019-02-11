import datetime
import logging

DATE_FORMAT = '%d.%m.%Y %H:%M%p'

logger = logging.getLogger()


def parse_date(date: str) -> datetime.datetime:
    if date is None:
        return None

    date: datetime = datetime.datetime.strptime(date, DATE_FORMAT)
    logger.debug("parsed date:{}".format(date))
    return date
