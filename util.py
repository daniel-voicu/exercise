from random import randint, uniform, shuffle
from time import sleep

_all_consumers_processed_ = False

MIN_AGE = 25
MAX_AGE = 55

MIN_NUMBER_OF_CARS = 0
MAX_NUMBER_OF_CARS = 3

MIN_NUMBER_OF_KIDS = 0
MAX_NUMBER_OF_KIDS = 3

MIN_HOUSEHOLD_INCOME = 125000
MAX_HOUSEHOLD_INCOME = 225000

MAX_SLEEP_BETWEEN_CALLS = 2  # seconds


def sleep_between_calls(max_sleep=MAX_SLEEP_BETWEEN_CALLS):
    sleep(uniform(0, max_sleep))


def random_interval(left, right):
    start = randint(left, right)
    end = randint(start, right)

    return (start, end)


def random_bool(chance_of_getting_true=50):
    """

    :param chance_of_getting_true:
    :return:
    """
    available_items = [True if i <= chance_of_getting_true else False for i in range(100)]
    shuffle(available_items)
    rand_index = randint(0, len(available_items) - 1)
    return available_items[rand_index]


def get_all_consumers_processed():
    global _all_consumers_processed_
    return _all_consumers_processed_


def set_all_consumers_processed(value):
    global _all_consumers_processed_
    _all_consumers_processed_ = value


def json_default(o):
    if hasattr(o, "__repr__"):
        return o.__repr__()
    raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')
