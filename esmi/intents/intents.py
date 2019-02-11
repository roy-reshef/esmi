import json
from _ast import Dict

from esmi.consts import ActionType


class Intent(object):

    def __init__(self, action: ActionType, entities: Dict):
        self.action = action
        self.entities = entities


class UserInputIntent(Intent):

    def __init__(self, action: ActionType, entities: Dict):
        Intent.__init__(self, action, entities)

    def __repr__(self):
        action = self.action.value if self.action is not None else ""
        return {
            'intent': 'user input',
            'action': action,
            'entities': self.entities,
        }

    def __str__(self):
        return json.dumps(self.__repr__(), indent=2)
