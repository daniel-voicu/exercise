from unittest import TestCase
from unittest.mock import MagicMock
from faker import Faker

from agent import Agent
from app import generate_agent, generate_consumer


class TestAgent(TestCase):

    def setUp(self):
        self.faker = Faker()
        self.agent = generate_agent(self.faker)
        self.consumer = generate_consumer(self.faker)

    def test_agent_creation(self):
        # Assert
        self.assertIsInstance(self.agent, Agent)

    def test_receive_call_set_available_false(self):
        # Act
        self.agent.receive_call(self.consumer)

        # Assert
        self.assertIs(self.agent.is_available, False)

    def test_make_call_should_call_consumer(self):
        # Arrange
        self.consumer.receive_call = MagicMock()

        # Act
        self.agent.make_call(self.consumer)

        # Assert
        self.consumer.receive_call.assert_called_with()

    def test_make_call_should_remove_consumer_from_inbox_if_consumer_available(self):
        # Arrange
        self.consumer.is_available = MagicMock(return_value=True)
        self.agent.voice_mail.remove_from_inbox = MagicMock()

        # Act
        self.agent.make_call(self.consumer)

        # Assert
        self.agent.voice_mail.remove_from_inbox.assert_called_with(self.consumer)

    def test_record_consumer_call_should_call_add_to_voice_mail_inbox(self):
        # Arrange
        self.agent.voice_mail.add_to_inbox = MagicMock()

        # Act
        self.agent.record_consumer_call(self.consumer)

        # Assert
        self.agent.voice_mail.add_to_inbox.assert_called_with(self.consumer)

    def test_match_by_attributes_should_call_specialize_match(self):
        # Arrange
        self.agent.specialize.match = MagicMock()

        # Act
        self.agent.match_by_attributes(self.consumer)

        # Assert
        self.agent.specialize.match.assert_called_with(self.consumer)
