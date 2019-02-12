from enum import Enum


class ActionType(Enum):
    CREATE = 1
    DELETE = 2
    EXIT = 3
    SHOW = 4


class Entities(Enum):
    ACTION = "ACTION"
    DATE = "DATE"
    LOCATION = "LOCATION"
    PURPOSE = "PURPOSE"
    ATTENDEES = "ATTENDEES"
    NUM_TO_SHOW = "NUM_TO_SHOW"


class ActionStatus(Enum):
    OK = 1,
    ERROR = 2
