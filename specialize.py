from util import interval_to_string


class Specialize(object):
    def __init__(self, age_range, state, number_of_kids_range, number_of_cars_range, owned_house,
                 household_income_range):
        self.age_range = age_range
        self.state = state
        self.number_of_kids_range = number_of_kids_range
        self.number_of_cars_range = number_of_cars_range
        self.owned_house = owned_house
        self.household_income_range = household_income_range

    def match(self, consumer):
        return self.__match_by_age(consumer.age) or self.__match_by_state(consumer.state) \
               or self.__match_by_number_of_kids(consumer.number_of_kids) or \
               self.__match_by_number_of_cars(consumer.number_of_cars) or \
               self.__match_by_owned_house(consumer.owned_house) or self.__match_by_household_income(
            consumer.household_income)

    def __match_by_age(self, age):
        return self.__value_in_interval(age, self.age_range)

    def __match_by_state(self, state):
        return state == self.state

    def __match_by_number_of_kids(self, number_of_kids):
        return self.__value_in_interval(number_of_kids, self.number_of_kids_range)

    def __match_by_number_of_cars(self, number_of_cars):
        return self.__value_in_interval(number_of_cars, self.number_of_cars_range)

    def __match_by_owned_house(self, owned_house):
        return owned_house == self.owned_house

    def __match_by_household_income(self, household_income):
        return self.__value_in_interval(household_income, self.household_income_range)

    def __value_in_interval(self, value, interval):
        return interval[0] <= value <= interval[1]

    def __repr__(self):
        return {"age range": interval_to_string(self.age_range), "state": self.state,
                "number of kids range": interval_to_string(self.number_of_kids_range),
                "number of cars": interval_to_string(self.number_of_cars_range), "owned house": self.owned_house,
                "household income range": interval_to_string(self.household_income_range)}
