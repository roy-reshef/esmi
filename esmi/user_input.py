import json
from typing import Dict


class RawUserInput(object):

    def __init__(self, entities: Dict):
        self.entities = entities

    def __repr__(self):
        return {
            'intent': 'user input',
            'entities': self.entities,
        }

    def __str__(self):
        return json.dumps(self.__repr__(), indent=2)
