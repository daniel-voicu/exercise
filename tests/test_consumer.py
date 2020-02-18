from unittest import TestCase

from faker import Faker
from mock import MagicMock

from app import generate_agent, generate_consumer
from router import Router


class TestConsumer(TestCase):

    def setUp(self):
        self.faker = Faker()
        self.agent = generate_agent(self.faker)
        self.consumer = generate_consumer(self.faker)
        self.router = Router([self.agent])

    def test_make_call_should_call_agency(self):
        # Arrange
        self.router.incoming_call = MagicMock()

        # Act
        self.consumer.make_call(self.router)

        # Assert
        self.router.incoming_call.assert_called_with(self.consumer)

    def test_receive_call_should_set_processed_to_true_if_consumer_available(self):
        # Arrange
        self.consumer.is_available = MagicMock(return_value=True)

        # Act
        self.consumer.receive_call()

        # Assert
        self.assertIs(self.consumer.processed, True)

    def test_receive_call_should_set_processed_to_false_if_consumer_not_available(self):
        # Arrange
        self.consumer.is_available = MagicMock(return_value=False)

        # Act
        self.consumer.receive_call()

        # Assert
        self.assertIs(self.consumer.processed, False)
