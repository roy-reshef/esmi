import logging

from esmi import calendar_client, consts, utils
from esmi.consts import Entities
from esmi.intents.intents import Intent

logger = logging.getLogger()


class IntentHandler(object):
    def __init__(self, intent: Intent):
        self.intent = intent

    def get_val(self, entity):
        return self.intent.entities[entity.value]

    def execute(self):
        logger.error("subclasses should override this function")


class CreateEventIntentHandler(IntentHandler):
    def __init__(self, intent: Intent):
        IntentHandler.__init__(self, intent)

    def execute(self):
        logger.info("handling event creation")

        # TODO: add validation
        date_str = self.get_val(Entities.DATE)
        date = None
        if date_str is not None:
            date = utils.parse_date(date_str)

        calendar_client.create_event(date,
                                     self.intent.entities[
                                         Entities.LOCATION.value],
                                     self.intent.entities[
                                         Entities.PURPOSE.value])


class ExitIntentHandler(IntentHandler):
    def __init__(self, intent: Intent):
        IntentHandler.__init__(self, intent)

    def execute(self):
        print("Bye for now")
        exit(0)


def handle_intent(intent: Intent):
    handler = None
    if intent.action is consts.ActionType.CREATE:
        handler = CreateEventIntentHandler(intent)
    elif intent.action is consts.ActionType.EXIT:
        handler = ExitIntentHandler(intent)

    if handler is None:
        logger.error("no intent handler was found for action:{}".format(
            intent.action.name))
    else:
        handler.execute()
