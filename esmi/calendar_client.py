from __future__ import print_function

import datetime
import logging
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# read/write access scope for events
# If modifying these scopes, delete the file token.pickle.
from esmi import env

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

logger = logging.getLogger()


def _get_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                env.GOOGLE_CREDS_FILE, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def get_next_events(num=10):
    service = _get_service()

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming {} events'.format(num))
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=num, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def get_upcoming_events():
    service = _get_service()

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    until = (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat() + 'Z'
    print('Getting the upcoming 24H events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          timeMax=until, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def create_event(starttime: datetime, location: str, purpose: str):
    endtime = starttime + datetime.timedelta(hours=1)

    print(starttime.day)
    date_format = '%Y-%m-%dT%H:%M:%S'
    event = {
        'summary': purpose,
        'description': purpose,
        'start': {
            'dateTime': starttime.strftime(date_format),
            'timeZone': 'Asia/Jerusalem',
        },
        'end': {
            'dateTime': endtime.strftime(date_format),
            'timeZone': 'Asia/Jerusalem',
        },
        # 'recurrence': [
        #     'RRULE:FREQ=DAILY;COUNT=1'
        # ],
        'attendees': [
            # {'email': 'lpage@example.com'},
            # {'email': 'sbrin@example.com'},
        ],
        'reminders': {
            'useDefault': True,
            # 'overrides': [
            #     {'method': 'email', 'minutes': 24 * 60},
            #     {'method': 'popup', 'minutes': 10},
            # ],
        },
    }
    if location:
        event['location'] = location

    event = _get_service().events().insert(calendarId='primary',
                                           body=event).execute()
    logger.info("event created: {}".format(event.get('htmlLink')))
