import datetime
import logging
import sys

import spacy
import json

from esmi.consts import Entities, ActionStatus
from esmi.input_providers import Terminal, Provider, Speech
from esmi.intents import intent_analysis, intent_handlers
from esmi.user_input import RawUserInput

logger = logging.getLogger()


def default_serializer(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def parse_user_input(nlp, user_input: str) -> RawUserInput:
    print('Input: {}'.format(user_input))
    doc = nlp(user_input)

    entities = {}

    for ent in doc.ents:
        logger.debug("text:{}, start:{}, end:{}, label:{}".format(ent.text,
                                                                  ent.start_char,
                                                                  ent.end_char,
                                                                  ent.label_))
        if ent.label_ == Entities.ACTION.value:
            entities[Entities.ACTION.value] = ent.text
        elif ent.label_ == Entities.DATE.value:
            entities[Entities.DATE.value] = ent.text
        elif ent.label_ == Entities.LOCATION.value:
            entities[Entities.LOCATION.value] = ent.text
        elif ent.label_ == Entities.PURPOSE.value:
            entities[Entities.PURPOSE.value] = ent.text
        elif ent.label_ == Entities.NUM_TO_SHOW.value:
            entities[Entities.NUM_TO_SHOW.value] = ent.text
        else:
            logger.warning(
                "unexpected label {} for value {}".format(ent.label_, ent.text))

    return RawUserInput(entities)


def get_input_provider() -> Provider:
    input_method = input(
        "would you like to use speech base input(y/<any-key>)\n")

    if input_method == 'y':
        input_provider = Speech()
    else:
        input_provider = Terminal()

    return input_provider


def print_welcome_message():
    print("Welcome to 'esmi' - Event Scheduling Management Interface")
    print("possible input examples:")
    print("create a meeting on 12.2.2019 9:00AM for fuseday at tikal")


def main(model_loc):
    nlp = spacy.load(model_loc)
    input_provider = get_input_provider()

    print_welcome_message()

    msg = "what can I do for you?\n"
    ctx = {"input_provider": Terminal()}

    while True:
        text = input_provider.get(msg)
        if text is not None:
            user_input = parse_user_input(nlp, text)
            logger.info("parsed user input: {}".format(json.dumps(user_input, default=default_serializer)))
            intent = intent_analysis.analyze_intent(user_input)
            logger.info(intent)
            res = intent_handlers.handle_intent(intent, ctx)
            if res.status == ActionStatus.OK:
                print("I happy to inform you that your wish came true")
                msg = "what can I do for you?\n"
            else:
                print(
                    "I'm sorry to inform you that I had difficulty performing "
                    "operation:{} ".format(res.message))
        else:
            msg = "please try again\n"


if __name__ == '__main__':
    main(sys.argv[1])
    # calendar_client.create_event(
    #     datetime.datetime.today() + datetime.timedelta(hours=1), "test")
    # calendar_client.get_next_events(10)
