from unittest import TestCase
from faker import Faker


from app import generate_consumer
from models.voice_mail import VoiceMail


class TestVoiceMail(TestCase):

    def setUp(self):
        self.faker = Faker()
        self.consumer = generate_consumer(self.faker)
        self.voice_mail = VoiceMail()
        self.voice_mail.inbox.append(self.consumer)

    def test_remove_from_inbox_should_remove_consumer(self):
        # Act
        self.voice_mail.remove_from_inbox(self.consumer)

        # Assert
        self.assertIs(len(self.voice_mail.inbox), 0)

    def test_add_to_inbox_should_add_consumer_to_inbox(self):
        # Arrange
        initial_count = len(self.voice_mail.inbox)

        # Act
        self.voice_mail.add_to_inbox(generate_consumer(self.faker))

        # Assert
        self.assertEqual(len(self.voice_mail.inbox), initial_count + 1)
