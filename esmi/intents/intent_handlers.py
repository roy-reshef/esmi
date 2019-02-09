import logging

from esmi import calendar_client, consts
from esmi.intents.intents import Intent

logger = logging.getLogger()


class IntentHandler(object):
    def __init__(self, intent: Intent):
        self.intent = intent

    def execute(self):
        logger.error("subclasses should override this function")


class CreateEventIntentHandler(IntentHandler):
    def __init__(self, intent: Intent):
        IntentHandler.__init__(self, intent)

    def execute(self):
        logger.info("handling event creation")
        calendar_client.create_event(self.intent.date, self.intent.location,
                                     self.intent.purpose)


def handle_intent(intent: Intent):
    handler = None
    if intent.action is consts.Action.CREATE:
        handler = CreateEventIntentHandler(intent)

    if handler is None:
        logger.error("no intent handler was found for action:{}".format(
            intent.action.name))
    else:
        handler.execute()
