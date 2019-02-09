import json


class RawUserInput(object):

    def __init__(self, action, date, location, purpose):
        self.action = action
        self.date = date
        self.location = location
        self.purpose = purpose

    def __repr__(self):
        return {
            'intent': 'user input',
            'action': self.action,
            'date': self.date,
            'location': self.location,
            'purpose': self.purpose
        }

    def __str__(self):
        return json.dumps(self.__repr__(), indent=2)
