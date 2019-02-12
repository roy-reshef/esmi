import logging

from esmi.consts import ActionType, Entities
from esmi.intents.intents import UserInputIntent
from esmi.user_input import RawUserInput

logger = logging.getLogger()


def _parse_action(action: str) -> ActionType:
    if action in {'set', 'create', 'new', 'invite', 'add', 'book', 'schedule'}:
        return ActionType.CREATE
    elif action in {'delete', 'remove', 'unset', 'unschedule'}:
        return ActionType.DELETE
    elif action in {'exit', 'quit'}:
        return ActionType.EXIT
    elif action in {'show', 'display'}:
        return ActionType.SHOW
    else:
        return None


def analyze_intent(user_input: RawUserInput) -> UserInputIntent:
    action = _parse_action(user_input.entities[Entities.ACTION.value])
    if action:
        return UserInputIntent(action, user_input.entities)
    return None
