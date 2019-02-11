import logging

from esmi import calendar_client, consts, utils
from esmi.consts import Entities, ActionStatus
from esmi.intents.intents import Intent

logger = logging.getLogger()


class ActionResponse(object):
    def __init__(self, status: ActionStatus, message=None):
        self.status = status
        self.message = message


class IntentHandler(object):
    def __init__(self, intent: Intent):
        self.intent = intent

    def get_val(self, entity):
        return self.intent.entities[entity.value]

    def execute(self) -> ActionResponse:
        raise Exception("IntentHandler Subclasses should implement execute")


class CreateEventIntentHandler(IntentHandler):
    def __init__(self, intent: Intent):
        IntentHandler.__init__(self, intent)

    def execute(self) -> ActionResponse:
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

        return ActionResponse(ActionStatus.OK)


class ExitIntentHandler(IntentHandler):
    def __init__(self, intent: Intent):
        IntentHandler.__init__(self, intent)

    def execute(self):
        print("Bye for now")
        exit(0)


def handle_intent(intent: Intent) -> ActionResponse:
    handler = None
    if intent.action is consts.ActionType.CREATE:
        handler = CreateEventIntentHandler(intent)
    elif intent.action is consts.ActionType.EXIT:
        handler = ExitIntentHandler(intent)

    if handler is None:
        logger.error("no intent handler was found for action:{}".format(
            intent.action.name))
        return ActionResponse(ActionStatus.ERROR,
                              "required action could not be resolved. "
                              "please try again")
    else:
        return handler.execute()
