#!/usr/bin/env python2

########
# Name: speech_manager.py
#
# Purpose: Manages speech input and intent recognition for the robot.
#
# Usage: Initialize this class and use the listen method to capture speech input, and the extract_intent method to determine the user's intent.
#
# Author: Pragna Guntupalli <sguntupalli@ucsd.edu>, Pranav Reddy Bussannagari <pbussannagari@ucsd.edu>
#
# Acknowledgements: The SpeechRecognition library and its documentation were instrumental in developing this module.
########

import re
import speech_recognition as sr


GREETING_PHRASES = (
    "hello",
    "hi",
    "hey",
    "excuse me",
    "robot",
)

GOODBYE_PHRASES = (
    "no thanks",
    "no thank you",
    "thank you",
    "thanks",
    "goodbye",
    "bye",
)

ROOM_QUERY_PHRASES = (
    "take me to",
    "bring me to",
    "lead me to",
    "navigate to",
    "go to",
    "where is",
    "where's",
    "find",
    "show me",
    "looking for",
)

ROOM_QUERY_KEYWORDS = (
    "room",
    "office",
    "lab",
    "commons",
    "lounge",
    "hallway",
    "corridor",
)

FILLER_PHRASES = (
    "can you",
    "could you",
    "would you",
    "please",
    "i want to",
    "i would like to",
    "i need to",
    "help me",
)


def normalize_text(text):
    text = str(text or "").lower()
    text = re.sub(r"[^a-z0-9'\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def contains_phrase(text, phrases):
    return any(re.search(r"\b%s\b" % re.escape(phrase), text) for phrase in phrases)


def strip_phrases(text, phrases):
    for phrase in phrases:
        text = re.sub(r"\b%s\b" % re.escape(phrase), " ", text)
    return re.sub(r"\s+", " ", text).strip()


class SpeechManager(object):
    def __init__(self):
        self.energy_threshold = None
        self.dynamic_energy_threshold = True
        self.use_microphone = True

    def listen(self, timeout_secs=7, phrase_limit=10, quiet_mode=False):
        if not self.use_microphone:
            return raw_input("User: ")

        return self.listen_for_command(timeout_secs, phrase_limit, quiet_mode)

    def listen_for_command(self, timeout_secs=7, phrase_limit=10, quiet_mode=False):
        recognizer = sr.Recognizer()
        recognizer.dynamic_energy_threshold = self.dynamic_energy_threshold

        if self.energy_threshold is not None:
            recognizer.energy_threshold = self.energy_threshold

        try:
            with sr.Microphone() as source:
                if self.dynamic_energy_threshold:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)

                audio = recognizer.listen(
                    source,
                    timeout=timeout_secs,
                    phrase_time_limit=phrase_limit
                )

            return recognizer.recognize_google(audio).lower()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return "unintelligible"
        except sr.RequestError:
            return None

    def extract_intent(self, text):
        text = normalize_text(text)

        if not text:
            return "unknown"
        if contains_phrase(text, GOODBYE_PHRASES):
            return "goodbye"
        if contains_phrase(text, ROOM_QUERY_PHRASES) or contains_phrase(text, ROOM_QUERY_KEYWORDS):
            return "room_query"
        if contains_phrase(text, GREETING_PHRASES):
            return "greeting"

        return "unknown"

    def extract_target(self, text):
        text = normalize_text(text)
        target = strip_phrases(text, FILLER_PHRASES)
        target = strip_phrases(target, ROOM_QUERY_PHRASES)
        target = re.sub(r"\b(the|a|an|please)\b", " ", target)
        target = re.sub(r"\s+", " ", target).strip()
        return target or text