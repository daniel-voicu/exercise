from datetime import datetime
from threading import Event
import logging
from faker import Faker

from generate_reports import generate_consumer_report
from models.router import Router
from models.consumer import Consumer
from models.agent import Agent
from models.specialize import Specialize
from util import MIN_AGE, MAX_AGE, MIN_NUMBER_OF_KIDS, MIN_NUMBER_OF_CARS, MAX_NUMBER_OF_CARS, MAX_NUMBER_OF_KIDS, \
    MIN_HOUSEHOLD_INCOME, MAX_HOUSEHOLD_INCOME, random_sleep_between_calls, random_interval, \
    set_all_consumers_processed, start_thread, CONSUMERS_COUNT, AGENTS_COUNT
from models.voice_mail import VoiceMail

logging.basicConfig(level=logging.INFO, format='(%(threadName)-9s) %(message)s', )

def generate_specialize(faker):
    return Specialize(age_range=random_interval(MIN_AGE, MAX_AGE),
                      state=faker.state(),
                      number_of_kids_range=random_interval(MIN_NUMBER_OF_KIDS, MAX_NUMBER_OF_KIDS),
                      number_of_cars_range=random_interval(MIN_NUMBER_OF_CARS, MAX_NUMBER_OF_CARS),
                      owned_house=faker.boolean(),
                      household_income_range=random_interval(MIN_HOUSEHOLD_INCOME, MAX_HOUSEHOLD_INCOME))


def generate_agent(faker):
    return Agent(
        id=faker.uuid4(),
        voice_mail=VoiceMail(),
        is_available=True,
        specialize=generate_specialize(faker)
    )


def generate_consumer(faker):
    return Consumer(
        id=faker.uuid4(),
        age=faker.random_int(MIN_AGE, MAX_AGE),
        state=faker.state(),
        number_of_kids=faker.random_int(MIN_NUMBER_OF_KIDS, MAX_NUMBER_OF_KIDS),
        number_of_cars=faker.random_int(MIN_NUMBER_OF_CARS, MAX_NUMBER_OF_CARS),
        owned_house=faker.boolean(),
        household_income=faker.random_int(MIN_HOUSEHOLD_INCOME, MAX_HOUSEHOLD_INCOME),
        phone_number=faker.phone_number(),
    )


def make_consumers_calls(consumers, router):
    threads = []
    for consumer in consumers:
        thread = start_thread(target=consumer.make_call, args=(router,), name=f"{consumer}")
        threads.append(thread)
        random_sleep_between_calls()

    for thread in threads:
        thread.join()


def check_for_processed_consumers(consumers, consumers_processed_event):
    unprocessed_consumers_count = len([consumer for consumer in consumers if not consumer.processed])
    while unprocessed_consumers_count > 0:
        random_sleep_between_calls()
        unprocessed_consumers_count = len([consumer for consumer in consumers if not consumer.processed])

    set_all_consumers_processed(True)
    consumers_processed_event.set()


if __name__ == "__main__":
    faker = Faker('en_US')

    start_date = datetime.now()
    consumers = [generate_consumer(faker) for i in range(CONSUMERS_COUNT)]
    agents = [generate_agent(faker) for i in range(AGENTS_COUNT)]
    router = Router(agents)

    consumers_processed_event = Event()
    router_thread = start_thread(target=router.run, args=(consumers_processed_event,))
    consumers_processed_thread = start_thread(target=check_for_processed_consumers,
                                              args=(consumers, consumers_processed_event,))

    consumers_thread = start_thread(target=make_consumers_calls, args=(consumers, router,))

    consumers_thread.join()
    router_thread.join()
    consumers_processed_thread.join()

    generate_consumer_report(consumers, agents)

    end_date = datetime.now()

    logging.info(f"Process finished in {end_date - start_date}")