from threading import Event
from unittest import TestCase

from faker import Faker
from mock import MagicMock

from app import generate_agent, generate_consumer
from models.router import Router


class TestRouter(TestCase):

    def setUp(self):
        self.faker = Faker()
        self.agent = generate_agent(self.faker)
        self.consumer = generate_consumer(self.faker)
        self.router = Router([self.agent])

    def test_find_agent_for_consumer_should_return_matching_agent(self):
        # Arrange
        self.agent.match_by_attributes = MagicMock(return_value=True)

        # Act
        agent = self.router.find_agent_for_consumer(self.consumer)

        # Assert
        self.assertEqual(agent, self.agent, f"{agent} is not equal with {self.agent}")

    def test_find_agent_for_consumer_should_return_none_if_no_matching_agent(self):
        # Arrange
        self.agent.match_by_attributes = MagicMock(return_value=False)

        # Act
        agent = self.router.find_agent_for_consumer(self.consumer)

        # Assert
        self.assertIs(agent, None)

    def test_find_agent_for_consumer_should_return_available_agent_when_matching_agents_available(self):
        # Arrange
        self.agent.match_by_attributes = MagicMock(return_value=True)
        self.agent.is_available = False

        new_agent = generate_agent(self.faker)
        new_agent.match_by_attributes = MagicMock(return_value=True)
        new_agent.is_available = True

        self.router.agents.append(new_agent)

        # Act
        agent = self.router.find_agent_for_consumer(self.consumer)

        # Assert
        self.assertEqual(agent, new_agent, f"{agent} is not equal with {new_agent}")

    def test_find_agent_for_consumer_should_return_an_unavailable_agent_when_no_matching_agents_available(self):
        # Arrange
        self.agent.match_by_attributes = MagicMock(return_value=True)
        self.agent.is_available = False

        new_agent = generate_agent(self.faker)
        new_agent.match_by_attributes = MagicMock(return_value=True)
        new_agent.is_available = False

        self.router.agents.append(new_agent)

        # Act
        agent = self.router.find_agent_for_consumer(self.consumer)

        # Assert
        self.assertIs(agent.is_available, False, f"{agent} is available")

    def test_incoming_call_should_pass_call_to_agent(self):
        # Arrange
        self.router.find_agent_for_consumer = MagicMock(return_value=self.agent)
        self.agent.handle_call = MagicMock()

        # Act
        self.router.incoming_call(self.consumer)

        # Assert
        self.agent.handle_call.assert_called_with(self.consumer)


    def test_run_should_initialize_agents(self):
        # Arrange
        self.agent.initialize = MagicMock()

        event_mock = Event()
        event_mock.isSet = MagicMock(return_value=True)

        # Act
        self.router.run(event_mock)

        # Assert
        self.agent.initialize.assert_called_with(event_mock)

    def test_pass_call_to_agent_should_set_agent_available_when_the_call_is_end(self):
        pass


