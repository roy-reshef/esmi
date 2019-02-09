import json

from esmi.consts import Action


class Intent(object):

    def __init__(self, action: Action):
        self.action = action


class UserInputIntent(Intent):

    def __init__(self, action: Action, date, location, purpose):
        Intent.__init__(self, action)
        self.date = date
        self.location = location
        self.purpose = purpose

    def __repr__(self):
        action = self.action.value if self.action is not None else ""
        date = str(self.date) if self.date is not None else ""
        return {
            'intent': 'user input',
            'action': action,
            'date': date,
            'location': self.location,
            'purpose': self.purpose
        }

    def __str__(self):
        return json.dumps(self.__repr__(), indent=2)
