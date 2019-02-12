import logging
from typing import Iterable

from esmi import calendar_client, consts, utils
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
        return self.intent.entities[entity.value]

    def execute(self) -> ActionResponse:
        raise Exception("IntentHandler Subclasses should implement execute")

    def required_entities(self) -> Iterable:
        raise Exception(
            "IntentHandler Subclasses should implement required_fields")

    def validate(self):
        for entity in self.required_entities():
            logger.debug("validating required entity:{}".format(entity))
            if entity not in self.intent.entities:
                logger.info("required entity:{} not found".format(entity))
                val = self.ctx['input_provider'].get(
                    "please provide value for {}\n".format(entity))

                logger.debug("provided val:{}".format(val))
                self.intent.entities[entity.value] = val


class CreateEventIntentHandler(IntentHandler):
    def __init__(self, intent: Intent, ctx):
        IntentHandler.__init__(self, intent, ctx)

    def execute(self) -> ActionResponse:
        logger.info("handling event creation")

        self.validate()
        print(self.intent)
        date_str = self.get_val(Entities.DATE)
        date = None
        if date_str is not None:
            date = utils.parse_date(date_str)

        calendar_client.create_event(date,
                                     self.intent.entities[
                                         Entities.LOCATION.value],
                                     self.intent.entities[
                                         Entities.PURPOSE.value])

        return ActionResponse(ActionStatus.OK)

    def required_entities(self) -> Iterable:
        return [Entities.LOCATION, Entities.DATE, Entities.PURPOSE]


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

    if handler is None:
        logger.error("no intent handler was found for action:{}".format(
            intent.action.name))
        return ActionResponse(ActionStatus.ERROR,
                              "required action could not be resolved. "
                              "please try again")
    else:
        return handler.execute()
