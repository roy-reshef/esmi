from enum import Enum


class ActionType(Enum):
    CREATE = 1
    DELATE = 2
    EXIT = 3


class Entities(Enum):
    ACTION = "ACTION"
    DATE = "DATE"
    LOCATION = "LOCATION"
    PURPOSE = "PURPOSE"
