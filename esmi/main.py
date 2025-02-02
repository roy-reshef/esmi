import datetime
import json
import logging
import sys

import spacy

from esmi.consts import Entities, ActionStatus
from esmi.input_providers import Terminal, Provider, Speech
from esmi.intents import intent_analysis, intent_handlers
from esmi.user_input import RawUserInput

logger = logging.getLogger()


def default_serializer(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def parse_user_input(nlp, user_input: str) -> RawUserInput:
    user_input = user_input.lower()
    logger.debug("User input %s", user_input)
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
                "Unexpected label {} for value {}".format(ent.label_, ent.text))

    return RawUserInput(entities)


def get_input_provider() -> Provider:
    input_method = input(
        "Would you like to use speech base input(y/<any-key>)\n")

    if input_method == 'y':
        input_provider = Speech()
    else:
        input_provider = Terminal()

    return input_provider


def print_welcome_message():
    print('      /\__\         /\__\         /\  \                  ')
    print('     /:/ _/_       /:/ _/_       |::\  \       ___       ')
    print('    /:/ /\__\     /:/ /\  \      |:|:\  \     /\__\      ')
    print('   /:/ /:/ _/_   /:/ /::\  \   __|:|\:\  \   /:/__/      ')
    print('  /:/_/:/ /\__\ /:/_/:/\:\__\ /::::|_\:\__\ /::\  \      ')
    print('  \:\/:/ /:/  / \:\/:/ /:/  / \:\~~\  \/__/ \/\:\  \__   ')
    print('   \::/_/:/  /   \::/ /:/  /   \:\  \        ~~\:\/\__\  ')
    print('    \:\/:/  /     \/_/:/  /     \:\  \          \::/  /  ')
    print('     \::/  /        /:/  /       \:\__\         /:/  /   ')
    print('      \/__/         \/__/         \/__/         \/__/    ')
    print('')
    print("Welcome to 'esmi' - Event Scheduling Management Interface")
    print("possible input examples:")
    print("create a meeting on 12.2.2019 9:00AM for fuseday at tikal")
    print("show \ display one \ upcoming events")
    print('')


def main(model_loc):
    nlp = spacy.load(model_loc)

    print_welcome_message()

    input_provider = get_input_provider()

    print('You are in {} mode'.format(input_provider.whoami()))

    msg = "What can I do for you?"
    ctx = {"input_provider": Terminal()}

    while True:
        text = input_provider.get(msg + '\n')
        if not text:
            msg = "Please try again"
            continue
        user_input = parse_user_input(nlp, text)
        logger.info("parsed user input: {}".format(
            json.dumps(user_input, default=default_serializer)))
        intent = intent_analysis.analyze_intent(user_input)
        if not intent:
            msg = "Please try again"
            continue
        logger.info(intent)
        res = intent_handlers.handle_intent(intent, ctx)
        if res.status == ActionStatus.OK:
            print("I happy to inform you that your wish came true")
            msg = "What can I do for you?"
        else:
            print("I'm sorry to inform you that I had difficulty performing "
                  "operation:{} ".format(res.message))


if __name__ == '__main__':
    main(sys.argv[1])
