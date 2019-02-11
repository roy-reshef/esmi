import logging

from esmi.consts import ActionType, Entities
from esmi.intents.intents import UserInputIntent
from esmi.user_input import RawUserInput

logger = logging.getLogger()


def _parse_action(action: str) -> ActionType:
    if action == 'set' or \
            action == 'create' or \
            action == 'new':
        return ActionType.CREATE
    elif action == 'delete' or \
            action == 'remove' or \
            action == 'unset':
        return ActionType.DELATE
    elif action == 'exit':
        return ActionType.EXIT
    else:
        return None


def analyze_intent(user_input: RawUserInput) -> UserInputIntent:
    action = _parse_action(user_input.entities[Entities.ACTION.value])
    return UserInputIntent(action, user_input.entities)
