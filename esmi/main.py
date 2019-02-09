import logging
import logging
import sys

import spacy

from esmi.input_providers import Terminal, Provider
from esmi.intents import intent_analysis, intent_handlers
from esmi.user_input import RawUserInput

logger = logging.getLogger()


def parse_user_input(nlp, user_input: str) -> RawUserInput:
    doc = nlp(user_input)

    action, date, location, purpose = None, None, None, None

    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)
        if ent.label_ == 'ACTION':
            action = ent.text
        elif ent.label_ == 'DATE':
            date = ent.text
        elif ent.label_ == 'LOCATION':
            location = ent.text
        elif ent.label_ == 'PURPOSE':
            purpose = ent.text
        else:
            logger.warning(
                "unexpected label {} for value {}".format(ent.label_, ent.text))

    return RawUserInput(action, date, location, purpose)


def get_input_provider() -> Provider:
    # input_method = input(
    #     "would you like to use speech base input(y/<eny-key>\n")
    #
    # if input_method == 'y':
    #     input_provider = Speech()
    # else:
    input_provider = Terminal()

    return input_provider


def print_welcome_message():
    print("Welcome to 'miri' - event scheduling personal assistant")
    print("possible input examples:")
    print("create a meeting on 12.2.2019 9:00AM for fuseday at tikal")
    # TODO: print all options


def main(model_loc):
    nlp = spacy.load(model_loc)
    input_provider = get_input_provider()

    print_welcome_message()

    user_input = input_provider.get("what can I do for you?\n")
    user_input = parse_user_input(nlp, user_input)
    logger.info("parsed user input: {}".format(user_input))
    intent = intent_analysis.analyze_intent(user_input)
    intent_handlers.handle_intent(intent)
    logger.info(intent)


if __name__ == '__main__':
    main(sys.argv[1])
    # calendar_client.create_event(
    #     datetime.datetime.today() + datetime.timedelta(hours=1), "test")
    # calendar_client.get_next_events(10)
