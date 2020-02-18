from unittest import TestCase
from faker import Faker
from app import generate_consumer, generate_specialize


class TestSpecialize(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.specialize = generate_specialize(self.faker)
        self.consumer = generate_consumer(self.faker)

    def test_match_should_return_true_when_only_state_is_matching(self):
        # Arrange
        self.__unmatch_consumer()
        self.consumer.state = self.specialize.state

        # Act
        # Assert
        self.assertIs(self.specialize.match(self.consumer), True,
                      f"Consumer state '{self.consumer.state}' not equal Specialize '{self.specialize.state}'")

    def test_match_should_return_true_when_only_age_range_is_matching(self):
        # Arrange
        self.__unmatch_consumer()
        self.consumer.age = self.specialize.age_range[1]

        # Act
        # Assert
        self.assertIs(self.specialize.match(self.consumer), True,
                      f"Consumer age '{self.consumer.age}' not in Specialize age range '{self.specialize.age_range}'")

    def test_match_should_return_true_when_only_number_of_kids_range_is_matching(self):
        # Arrange
        self.__unmatch_consumer()
        self.consumer.number_of_kids = self.specialize.number_of_kids_range[0]

        # Act
        # Assert
        self.assertIs(self.specialize.match(self.consumer), True,
                      f"Consumer number of kids '{self.consumer.number_of_kids}' not in Specialize number of kids range '{self.specialize.number_of_kids_range}'")

    def test_match_should_return_true_when_only_number_of_cars_range_is_matching(self):
        # Arrange
        self.__unmatch_consumer()
        self.consumer.number_of_cars = self.specialize.number_of_cars_range[1]

        # Act
        # Assert
        self.assertIs(self.specialize.match(self.consumer), True,
                      f"Consumer number of cars '{self.consumer.number_of_cars}' not in Specialize number of cars range '{self.specialize.number_of_cars_range}'")

    def test_match_should_return_true_when_only_owned_house_is_matching(self):
        # Arrange
        self.__unmatch_consumer()
        self.consumer.owned_house = self.specialize.owned_house

        # Act
        # Assert
        self.assertIs(self.specialize.match(self.consumer), True,
                      f"Consumer owned house '{self.consumer.owned_house}' not equal Specialize owned house '{self.specialize.owned_house}'")

    def test_match_should_return_true_when_only_household_income_range_is_matching(self):
        # Arrange
        self.__unmatch_consumer()
        self.consumer.household_income = self.specialize.household_income_range[1]

        # Act
        # Assert
        self.assertIs(self.specialize.match(self.consumer), True,
                      f"Consumer household income '{self.consumer.household_income}' not in Specialize household income range '{self.specialize.household_income_range}'")

    def __unmatch_consumer(self):
        self.consumer.age = self.specialize.age_range[1] + 10
        self.consumer.state = f"Test {self.specialize.state}"
        self.consumer.number_of_kids = self.specialize.number_of_kids_range[1] + 1
        self.consumer.number_of_cars = self.specialize.number_of_cars_range[1] + 1
        self.consumer.owned_house = not self.specialize.owned_house
        self.household_income = self.specialize.household_income_range[1] + 10
