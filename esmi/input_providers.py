import abc

import speech_recognition as sr
from speech_recognition import AudioData


class Provider(object):
    @abc.abstractmethod
    def get(self, prompt: str) -> str:
        pass

    @abc.abstractmethod
    def whoami(self) -> str:
        pass


class Speech(Provider):

    def whoami(self) -> str:
        return 'Speech Mode'

    def __init__(self):
        print("running speech recognition version:", sr.__version__)

    def get(self, prompt: str) -> str:
        r = sr.Recognizer()
        mic = sr.Microphone()

        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        print(prompt)
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio: AudioData = r.listen(source)

            try:
                response["transcription"] = r.recognize_google(audio)
            except sr.RequestError:
                # API was unreachable or unresponsive
                response["success"] = False
                response["error"] = "API unavailable"
            except sr.UnknownValueError:
                # speech was unintelligible
                response["error"] = "Unable to recognize speech"

        return response["transcription"]


class Terminal(Provider):

    def get(self, prompt: str) -> str:
        return input(prompt)

    def whoami(self) -> str:
        return 'Text Mode'
