class Agent(object):
    def __init__(self, id, voice_mail, is_available, specialize):
        self.id = id
        self.voice_mail = voice_mail
        self.is_available = is_available
        self.specialize = specialize

        # used to generate report
        self.total_calls_received = 0

    def receive_call(self, consumer):
        self.total_calls_received += 1
        self.is_available = False

    def make_call(self, consumer):
        self.is_available = False
        consumer.receive_call()
        if consumer.processed:
            self.voice_mail.remove_from_inbox(consumer)
        self.is_available = True

    def record_consumer_call(self, consumer):
        self.voice_mail.add_to_inbox(consumer)

    def match_by_attributes(self, consumer):
        return self.specialize.match(consumer)

    def __repr__(self):
        return {"id": self.id, "specialize": self.specialize.__dict__, "voice mail": self.voice_mail.__dict__,
                "total calls received": self.total_calls_received}

    def __str__(self):
        return f"Agent {self.id}"
