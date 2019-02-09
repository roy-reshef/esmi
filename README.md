# Overview
conversational based personal assistant for event scheduling using google calendar

# Installation
* debian based linux OS - run install.sh script. this script install required audio packages in addition to python modules.
* other OS - install required python packages found in requirements.txt file, run other commands that are found
in installation script and see 'Speech Recognition' documentation

## google calendar API
Follow instructions [here](https://developers.google.com/calendar/quickstart/python) to produce credentials file

# Model generation

run create_model.sh <path_to_model_output_dir>
training data can be found in _train_data.py_ file

# Runninng
execute miri.py <path_to_generated model>

**env variables**
* GOOGLE_CREDS - path to google credentials file

**internet connection is required** for using google APIs. 

Speech recognition is using Google API. For other speech recognition endpoints see 'speech recognition' library

# What's next?
* manage context and manage session with user
* event time duration
* more training data
* implement event deletion and update
* better date recognition
* additional event entities (attendees, reminders)
* enable speech recognition
* text to speech

# Technical References

## spacy NLP Library
https://spacy.io/

## Speech Recognition
https://realpython.com/python-speech-recognition/

## Calendar API references
**Create events:** https://developers.google.com/calendar/create-events?authuser=1

## Text To Speech
https://pythonprogramminglanguage.com/text-to-speech/

## python date formatting
in order to support more date formats
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior