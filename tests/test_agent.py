from unittest import TestCase
from unittest.mock import MagicMock
from faker import Faker

from models.agent import Agent
from app import generate_agent, generate_consumer


class TestAgent(TestCase):

    def setUp(self):
        self.faker = Faker()
        self.agent = generate_agent(self.faker)
        self.consumer = generate_consumer(self.faker)

    def test_agent_creation(self):
        # Assert
        self.assertIsInstance(self.agent, Agent)

    def test_handle_call_increase_total_calls_received(self):
        # Assert
        initial_value = self.agent.total_calls_received

        # Act
        self.agent.handle_call(self.consumer)

        # Assert
        self.assertEqual(self.agent.total_calls_received, initial_value + 1)

    def test_make_call_should_call_consumer(self):
        # Arrange
        self.consumer.receive_call = MagicMock()

        # Act
        self.agent.make_call(self.consumer)

        # Assert
        self.consumer.receive_call.assert_called_with()

    def test_match_by_attributes_should_call_specialize_match(self):
        # Arrange
        self.agent.specialize.match = MagicMock()

        # Act
        self.agent.match_by_attributes(self.consumer)

        # Assert
        self.agent.specialize.match.assert_called_with(self.consumer)
