import threading
import logging

from util import random_sleep_between_calls


class Agent(object):
    def __init__(self, id, voice_mail, is_available, specialize):
        self.id = id
        self.voice_mail = voice_mail
        self.is_available = is_available
        self.specialize = specialize
        self.total_calls_received = 0
        self.outbound_calls_history = {}

        self.__lock = threading.Lock()

    def handle_call(self, consumer):
        self.__increase_total_calls_received()

        if self.__check_and_attempt_set_is_available():
            random_sleep_between_calls()
            consumer.processed = True
            self.__set_is_available(True)
            logging.info(f"{consumer} processed by agent {self}")
        else:
            logging.info(f"Add {consumer} to {self} queue")
            self.add_call_to_queue(consumer)

    def make_call(self, consumer):
        consumer.receive_call()

    def add_call_to_queue(self, consumer):
        self.voice_mail.add_to_inbox(consumer)

    def match_by_attributes(self, consumer):
        return self.specialize.match(consumer)

    def initialize(self, consumers_processed_event):
        while not consumers_processed_event.isSet():
            for consumer in self.voice_mail.inbox:
                self.__process_queue_item(consumer)

    def __increase_total_calls_received(self):
        self.__lock.acquire()
        try:
            self.total_calls_received += 1
        finally:
            self.__lock.release()

    def __record_outbound_call_attempt(self, consumer_id):
        if consumer_id in self.outbound_calls_history.keys():
            self.outbound_calls_history[consumer_id] += 1
        else:
            self.outbound_calls_history[consumer_id] = 1

    def __process_queue_item(self, consumer):
        if self.__check_and_attempt_set_is_available():
            self.__record_outbound_call_attempt(consumer.id)
            self.make_call(consumer)
            if consumer.processed:
                self.voice_mail.remove_from_inbox(consumer)
                logging.info(f"{consumer} was processed by {self}")

            random_sleep_between_calls()
            self.__set_is_available(True)

    def __set_is_available(self, value):
        self.__lock.acquire()
        try:
            self.is_available = value
        finally:
            self.__lock.release()

    def __check_and_attempt_set_is_available(self):
        self.__lock.acquire()
        initial_value = self.is_available
        try:
            self.is_available = not self.is_available
        finally:
            self.__lock.release()
        return initial_value

    def __repr__(self):
        return {"id": self.id, "specialize": self.specialize.__dict__, "voice mail": self.voice_mail.__dict__,
                "total calls received": self.total_calls_received}

    def __str__(self):
        return f"Agent {self.id}"
