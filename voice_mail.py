class VoiceMail(object):
    def __init__(self):
        self.inbox = []
        self.total_voicemails_left = 0.

    def remove_from_inbox(self, consumer):
        self.inbox.remove(consumer)

    def add_to_inbox(self, consumer):
        self.total_voicemails_left += 1
        self.inbox.append(consumer)


    def __repr__(self):
        return {"total voicemails left": self.total_voicemails_left}
