# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

import os
import json
import datetime
import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted
from requests import ConnectionError, HTTPError, TooManyRedirects, Timeout


logger = logging.getLogger(__name__)
REQUESTED_SLOT = "requested_slot"


class AdmissionLetterForm(FormAction):

    def __init__(self):
        self.letter_mapping = {
            '山西': '已寄出',
            '陕西': '7月9日寄出',
            '山东': '7月10日寄出',
            '黑龙江': '已寄出',
            '吉林': '7月3日寄出',
            '辽宁': '7月4日寄出',
            '河北': '已寄出',
            '北京': '已寄出',
            '天津': '7月8日寄出',
            '新疆': '已寄出',
            '西藏': '已寄出',
            '青海': '已寄出',
            '甘肃': '7月7日寄出',
            '四川': '已寄出',
            '云南': '7月9日寄出',
            '广西': '7月8日寄出',
            '安徽': '已寄出',
            '江苏': '已寄出',
            '重庆': '7月5日寄出',
            '浙江': '已寄出',
            '上海': '已寄出',
            '湖北': '7月10日寄出',
            '湖南': '已寄出',
            '福建': '已寄出',
            '广东': '7月8日寄出',
            '海南': '7月9日寄出',
            '河南': '已寄出',
            '内蒙古': '已寄出',
            '宁夏': '7月6日寄出',
            '贵州': '7月4日寄出',
            '江西': '已寄出',
        }

    def name(self) -> Text:
        return "admission_letter_form"

    @staticmethod
    def required_slots(tracker):
        return ["address"]

    def slot_mapping(self):
        return {
            "address": self.from_entity(entity="address")
        }

    def submit(self, dispatcher, tracker, domain):
        intent = tracker.latest_message['intent'].get('name')
        address = tracker.get_slot("address")
        letter_msg = self.letter_mapping[address]
        text_message = "你好, {}的通知书{}".format(address, letter_msg)
        dispatcher.utter_message(text_message)
        return [SlotSet("address", None)]



class AdmissionResultForm(FormAction):

    def __init__(self):
        self.enroll_result = {
            ('2033451871', '张三', '上海', '400'): '计算机专业',
            ('2033451872', '李四', '北京', '500'): '土木工程专业',
            ('2033451873', '王五', '江苏', '600'): '师范专业',
        }

    def name(self) -> Text:
        return "admission_result_form"

    @staticmethod
    def required_slots(tracker):
        return ["address", "number", "name", "score"]

    def slot_mapping(self):
        return {
            "address": self.from_entity(entity="address"),
            "number": self.from_entity(entity="number"),
            "name": self.from_entity(entity="name"),
            "score": self.from_entity(entity="score"),
        }

    def submit(self, dispatcher, tracker, domain):
        address = tracker.get_slot("address")
        number = tracker.get_slot("number")
        name = tracker.get_slot("name")
        score = tracker.get_slot("score")
        result = self.enroll_result.get((number, name, address, score))
        if result:
            text_message = "专业是{}".format(result)
            dispatcher.utter_message(text_message)
        else:
            text_message = "未查询到你的录取信息，请核实输入信息是否正确"
            dispatcher.utter_message(text_message)
        return [SlotSet("address", None),
                SlotSet("number", None),
                SlotSet("name", None),
                SlotSet("score", None)]

class ActionSlotReset(Action):
    def name(self):
        return 'action_slot_reset'

    def run(self, dispatcher, tracker, domain):
        return[AllSlotsReset(), Restarted()]

