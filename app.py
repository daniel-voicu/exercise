from threading import Thread

from faker import Faker
from router import Router
from consumer import Consumer
from agent import Agent
from specialize import Specialize
from util import MIN_AGE, MAX_AGE, MIN_NUMBER_OF_KIDS, MIN_NUMBER_OF_CARS, MAX_NUMBER_OF_CARS, MAX_NUMBER_OF_KIDS, \
    MIN_HOUSEHOLD_INCOME, MAX_HOUSEHOLD_INCOME, sleep_between_calls, random_interval, set_all_consumers_processed
from voice_mail import VoiceMail


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
    for consumer in consumers:
        print(f"{consumer} will call to agency")
        consumer.make_call(router)
        sleep_between_calls()


def check_for_processed_consumers(consumers):
    unprocessed_consumers_count = len([consumer for consumer in consumers if not consumer.processed])
    while unprocessed_consumers_count > 0:
        sleep_between_calls(1)
        unprocessed_consumers_count = len([consumer for consumer in consumers if not consumer.processed])

    set_all_consumers_processed(True)


if __name__ == "__main__":
    faker = Faker('en_US')

    consumers = [generate_consumer(faker) for i in range(10)]
    agents = [generate_agent(faker) for i in range(2)]
    router = Router(agents)

    consumers_processed_thread = Thread(target=check_for_processed_consumers, args=(consumers, ))
    consumers_processed_thread.setDaemon(True)
    consumers_processed_thread.start()

    consumers_thread = Thread(target=make_consumers_calls, args=(consumers, router,))
    consumers_thread.setDaemon(True)
    consumers_thread.start()

    router_thread = Thread(target=router.run, args=())
    router_thread.setDaemon(True)
    router_thread.start()

    consumers_thread.join()
    router_thread.join()
    consumers_processed_thread.join()

    sleep_between_calls()
