from random import randint, uniform, shuffle
from threading import Thread
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

MAX_SLEEP_BETWEEN_CALLS = 3  # seconds

AGENTS_COUNT = 20
CONSUMERS_COUNT = 1000


def random_sleep_between_calls(min_sleep=0, max_sleep=MAX_SLEEP_BETWEEN_CALLS):
    """
    Suspends the execution of the current thread for a random amount of seconds.
    :param min_sleep: minim amount of seconds to sleep
    :param max_sleep: maxim amount of seconds to sleep
    :return:
    """
    sleep(uniform(min_sleep, max_sleep))


def random_interval(left, right):
    """
    Generates a random interval based on a start end value
    :param left: minim value for interval
    :param right: maxim value for interval
    :return: interval as tuple
    :raise: ValueError if left value greater than right value
    """

    if left > right:
        raise ValueError(f"Left value '{left}' of interval cannot be greater than the right value '{right}'")

    start = randint(left, right)
    end = randint(start, right)

    return (start, end)


def random_bool(chance_of_getting_true=50):
    """
    Generates a random bool value.
    :param chance_of_getting_true: change of getting true can be increased/decreased using this value
    :return: random bool value
    """
    available_items = [True if i <= chance_of_getting_true else False for i in range(100)]
    shuffle(available_items)
    rand_index = randint(0, len(available_items) - 1)
    return available_items[rand_index]


def get_all_consumers_processed():
    """
    Getter for global variable _all_consumers_processed_
    :return: value of _all_consumers_processed_
    """
    global _all_consumers_processed_
    return _all_consumers_processed_


def start_thread(target, args, name=None):
    """
    Start a new thread with the received parameters
    :param target: method to be executed inside thread
    :param args: parameters for target
    :param name: name of thread
    :return: newly created thread
    """
    thread = Thread(name=name, target=target, args=args)
    thread.setDaemon(True)
    thread.start()
    return thread

def interval_to_string(value):
    return f"{value[0]} - {value[1]}"

def set_all_consumers_processed(value):
    """
    Setter for global variable _all_consumers_processed_
    :param value: new value for _all_consumers_processed_
    :return:
    """
    global _all_consumers_processed_
    _all_consumers_processed_ = value
