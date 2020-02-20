import logging
from random import randint
from typing import List

from agent import Agent
from util import start_thread


class Router(object):
    def __init__(self, agents: List[Agent]):
        self.agents = agents

    def run(self, consumers_processed_event):
        agent_threads = []
        for agent in self.agents:
            thread = start_thread(target=agent.initialize, args=(consumers_processed_event,), name=f"{agent}")
            agent_threads.append(thread)

        for thread in agent_threads:
            thread.join()

    def __find_available_agents_with_inbox_items(self):
        return [agent for agent in self.agents if agent.is_available and len(agent.voice_mail.inbox) > 0]

    def incoming_call(self, consumer):
        agent = self.find_agent_for_consumer(consumer)

        agent.handle_call(consumer)

    def find_agent_for_consumer(self, consumer):
        # Each consumer has a set of attributes that determine how they are matched with the agents.
        # Each agent has a set of attributes that determine they can be matched with consumers with certain attributes.
        # If multiple agents match a consumer’s attributes then an agent is picked at random

        matching_agents = [agent for agent in self.agents if agent.match_by_attributes(consumer)]
        matching_agents_len = len(matching_agents)

        if matching_agents_len == 0:
            logging.error(f"Unable to find a matching agent for {consumer}. Passing it to a random agent")
            return self.agents[randint(0, len(self.agents) - 1)]

        return matching_agents[randint(0, matching_agents_len - 1)]
