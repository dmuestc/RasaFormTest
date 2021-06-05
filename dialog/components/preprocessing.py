#coding=utf-8

import re
import json
import datetime
import numpy as np
from typing import Any, Dict, Optional, Text
from rasa.nlu.components import Component
from rasa.nlu.constants import ENTITIES
from LAC import LAC


class PreprocessAnalyzer(Component):
    """A user-defined preprosssing component"""

    name = "IntentAnalyzer"
    requires = []
    defaults = {}
    language_list = ["zh"]

    def __init__(self, component_config=None):
        super(PreprocessAnalyzer, self).__init__(component_config)

        # default user
        self.default_user = "user"
        self.lac = LAC(mode="lac")

        # default intent
        self.default_intent = "default"
        self.provs = ["北京", "上海", "江苏"]

        self.greet_goodbye = {}
        with open('./data/greet_goodbye.md', "r", encoding="utf8") as fg:
            for line in fg.readlines():
                content = line.strip()
                if content == "":
                    continue
                if content[0] == "#":
                    p = content.split(":")[1].strip()
                    self.greet_goodbye[p] = []
                else:
                    content = content.split("-")[1].strip()
                    self.greet_goodbye[p].append(content)

    def get_address(self, text):
        for k in self.provs:
            if k in text:
                return k
        return None

    def is_goodbye(self, text):
        text = text.strip().lower()
        if text in self.greet_goodbye["goodbye"]:
            return True

    def is_greet(self, text):
        text = text.strip().lower()
        if text in self.greet_goodbye["greet"]:
            return True

    def process(self, message, **kwargs):

        if self.is_goodbye(message.text):
            intent_json = {'name': "goodbye", "confidence": 1.0}
        elif self.is_greet(message.text):
            intent_json = {'name': "greet", "confidence": 1.0}
        elif "通知书" in message.text:
            intent_json = {'name': "admission_letter", "confidence": 1.0}
        elif "录取" in message.text:
            intent_json = {'name': "admission_result", "confidence": 1.0}
        else:
            intent_json = {'name': "default", "confidence": 1.0}

        address = self.get_address(message.text) 
        number = re.findall(r"\d{7,12}", message.text)
        score = re.findall(r"\d{2,3}", message.text)
        ner_res = self.lac.run(message.text)
        #print(address, number, score, intent_json)

        name = ""
        for word, tag in zip(ner_res[0], ner_res[1]):
            if tag == "PER":
                name = word
                break

        entities = []
        if address:
            entities.append(
                {"entity": "address", "value": address, "confidence": 1}
            )

        if len(number) == 1:
            entities.append(
                {"entity": "number", "value": number[0], "confidence": 1}
            )

        if len(score) == 1:
            entities.append(
                {"entity": "score", "value": score[0], "confidence": 1}
            )

        if name != "":
            entities.append(
                {"entity": "name", "value": name, "confidence": 1}
            )

        message.set(
            "entities", message.get(ENTITIES, []) + entities, add_to_output=True
        )
        message.set('intent', intent_json, add_to_output=True)

