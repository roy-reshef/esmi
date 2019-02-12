import logging
from typing import Iterable

from word2number import w2n

from esmi import calendar_client, consts
from esmi import utils
from esmi.consts import Entities, ActionStatus
from esmi.intents.intents import Intent

logger = logging.getLogger()


class ActionResponse(object):
    def __init__(self, status: ActionStatus, message=None):
        self.status = status
        self.message = message


class IntentHandler(object):
    def __init__(self, intent: Intent, ctx):
        self.intent = intent
        self.ctx = ctx

    def get_val(self, entity):
        return self.intent.entities.get(entity.value)

    def execute(self) -> ActionResponse:
        raise Exception("IntentHandler Subclasses should implement execute")

    def required_entities(self) -> Iterable:
        raise Exception(
            "IntentHandler Subclasses should implement required_fields")

    def validate(self):
        for entity in self.required_entities():
            logger.debug("validating required entity:{}".format(entity))
            if entity.value not in self.intent.entities:
                logger.info("required entity:{} not found".format(entity))
                val = self.ctx['input_provider'].get(
                    "please provide value for {}\n".format(entity))

                logger.debug("provided val:{}".format(val))
                self.intent.entities[entity.value] = val


# class CreateEventIntentHandler(IntentHandler):
#     def __init__(self, intent: Intent, ctx):
#         IntentHandler.__init__(self, intent, ctx)
#
#     def execute(self) -> ActionResponse:
#         logger.info("handling event creation")
#
#         # self.validate()
#         date_str = self.get_val(Entities.DATE)
#         date = None
#         if date_str:
#             if isinstance(date_str, datetime.datetime):
#                 date = date_str
#             if isinstance(date_str, str):
#                 date = dateparser.parse(date_str)
#
#         calendar_client.create_event(date,
#                                      self.intent.entities[
#                                          Entities.LOCATION.value],
#                                      self.intent.entities[
#                                          Entities.PURPOSE.value])
#
#         return ActionResponse(ActionStatus.OK)
#
#     def required_entities(self) -> Iterable:
#         return [Entities.LOCATION, Entities.DATE, Entities.PURPOSE]

class CreateEventIntentHandler(IntentHandler):
    def __init__(self, intent: Intent, ctx):
        IntentHandler.__init__(self, intent, ctx)

    def execute(self) -> ActionResponse:
        logger.info("handling event creation")

        self.validate()
        date_str = self.get_val(Entities.DATE)
        date = None
        if date_str is not None:
            date = utils.parse_date(date_str)

        try:
            calendar_client.create_event(date,
                                         self.intent.entities.get(Entities.LOCATION.value),
                                         self.intent.entities.get(Entities.PURPOSE.value)
                                         )
            return ActionResponse(ActionStatus.OK)
        except:
            return ActionResponse(ActionStatus.ERROR)

    def required_entities(self) -> Iterable:
        return [Entities.LOCATION, Entities.DATE, Entities.PURPOSE]


class ShowEventIntentHandler(IntentHandler):
    def __init__(self, intent: Intent, ctx):
        IntentHandler.__init__(self, intent, ctx)

    def execute(self) -> ActionResponse:
        logger.info("handling events display")

        self.validate()
        num_of_events = self.get_val(Entities.NUM_TO_SHOW)
        if num_of_events:
            try:
                events_count = w2n.word_to_num(num_of_events)
                calendar_client.get_next_events(events_count)
            except ValueError:
                if num_of_events == 'upcoming':
                    calendar_client.get_upcoming_events()
                elif num_of_events.isnumeric():
                    calendar_client.get_next_events(num_of_events)
        return ActionResponse(ActionStatus.OK)

    def required_entities(self) -> Iterable:
        return [Entities.NUM_TO_SHOW]


class ExitIntentHandler(IntentHandler):
    def __init__(self, intent: Intent, ctx):
        IntentHandler.__init__(self, intent, ctx)

    def execute(self):
        print("Bye for now")
        exit(0)


def handle_intent(intent: Intent, ctx) -> ActionResponse:
    handler = None
    if intent.action is consts.ActionType.CREATE:
        handler = CreateEventIntentHandler(intent, ctx)
    elif intent.action is consts.ActionType.EXIT:
        handler = ExitIntentHandler(intent, ctx)
    elif intent.action is consts.ActionType.SHOW:
        handler = ShowEventIntentHandler(intent, ctx)

    if handler is None:
        logger.error("no intent handler was found for action:{}".format(
            intent.action.name))
        return ActionResponse(ActionStatus.ERROR,
                              "required action could not be resolved. "
                              "please try again")
    else:
        return handler.execute()
