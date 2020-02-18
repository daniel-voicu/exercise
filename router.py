from random import randint
from threading import Thread
from typing import List

from agent import Agent
from util import sleep_between_calls, get_all_consumers_processed


class Router(object):
    def __init__(self, agents: List[Agent]):
        self.agents = agents

    def run(self):
        agents_with_inbox_items = self.__find_available_agents_with_inbox_items()
        while not get_all_consumers_processed():
            for agent in agents_with_inbox_items:
                # agent.handle_missing_calls()
                # TODO move the logic to create threads to a method
                for consumer in agent.voice_mail.inbox:
                    thread = Thread(target=self.initiate_agent_call_to_consumer, args=(consumer, agent))
                    thread.setDaemon(True)
                    thread.start()

            agents_with_inbox_items = [agent for agent in self.agents if len(agent.voice_mail.inbox) > 0]

    def __find_available_agents_with_inbox_items(self):
        return [agent for agent in self.agents if agent.is_available and len(agent.voice_mail.inbox) > 0]

    def incoming_call(self, consumer):
        print(f"Incoming call from {consumer}")
        agent = self.find_agent_for_consumer(consumer)

        if agent is None:
            print(f"Unable to find an agent for {consumer}")
            return

        if agent.is_available:
            thread = Thread(target=self.pass_call_to_agent, args=(agent, consumer,))
            thread.start()
        else:
            print(f"{agent} is not available. {consumer} will be added to inbox")
            agent.record_consumer_call(consumer)

    def pass_call_to_agent(self, agent, consumer):
        agent.receive_call(consumer)
        print(f"{agent} received call from {consumer}")
        sleep_between_calls()
        agent.is_available = True
        consumer.processed = True

    def initiate_agent_call_to_consumer(self, consumer, agent):
        print(f"{agent} will call {consumer}")
        agent.make_call(consumer)
        sleep_between_calls()

    def find_agent_for_consumer(self, consumer):
        # Each consumer has a set of attributes that determine how they are matched with the agents.
        # Each agent has a set of attributes that determine they can be matched with consumers with certain attributes.
        # If multiple agents match a consumer’s attributes then an agent is picked at random

        matching_agents = [agent for agent in self.agents if agent.match_by_attributes(consumer)]
        matching_agents_len = len(matching_agents)

        if matching_agents_len == 0:
            return None

        available_agents = [agent for agent in matching_agents if agent.is_available]
        if len(available_agents) == 0:
            return matching_agents[0]
        else:
            return available_agents[randint(0, len(available_agents) - 1)]
