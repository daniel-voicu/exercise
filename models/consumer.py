from util import random_bool


class Consumer(object):
    def __init__(self, id, age, state, number_of_kids, number_of_cars, owned_house, household_income, phone_number,
                 processed=False):
        self.id = id
        self.age = age
        self.state = state
        self.number_of_kids = number_of_kids
        self.number_of_cars = number_of_cars
        self.owned_house = owned_house
        self.household_income = household_income
        self.phone_number = phone_number
        self.processed = processed

    def make_call(self, agency):
        agency.incoming_call(self)

    def receive_call(self):
        if self.is_available():
            self.processed = True

    def is_available(self):
        return random_bool(chance_of_getting_true=80)

    def __repr__(self):
        return {"id": self.id, "age": self.age, "state": self.state, "number of kids": self.number_of_kids,
                "number of cars": self.number_of_cars, "owned house": self.owned_house,
                "household income": self.household_income, "phone_number": self.phone_number,
                "processed": self.processed}

    def __str__(self):
        return f"Consumer {self.__repr__()['id']}"
