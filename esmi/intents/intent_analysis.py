import datetime
import logging

from esmi.consts import Action
from esmi.intents.intents import UserInputIntent
from esmi.user_input import RawUserInput

DATE_FORMAT = '%d.%m.%Y %H:%M%p'

logger = logging.getLogger()


def _parse_date(date: str) -> datetime.datetime:
    if date is None:
        return None

    date: datetime = datetime.datetime.strptime(date, DATE_FORMAT)
    logger.debug("parsed date:{}".format(date))
    return date


def _parse_action(action: str) -> Action:
    if action == 'set' or \
            action == 'create' or \
            action == 'new':
        return Action.CREATE
    elif action == 'delete' or \
            action == 'remove' or \
            action == 'unset':
        return Action.DELATE
    else:
        return None


def analyze_intent(user_input: RawUserInput) -> UserInputIntent:
    action = _parse_action(user_input.action)
    return UserInputIntent(action,
                           _parse_date(user_input.date),
                           user_input.location,
                           user_input.purpose)
