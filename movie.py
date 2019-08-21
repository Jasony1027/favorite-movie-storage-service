from sqlalchemy import Column, Integer, String, Float
from abstract_entertainment import AbstractEntertainment


class Movie(AbstractEntertainment):
    """ Movie Class - Maintains the details of each movie """

    ENT_TYPE = "Movie"

    length = Column(Float(3))

    def __init__(self, id, name, year_released, director, rating, type, length):
        """ Constructor - Initializes the main attributes for the movie """
        super().__init__(id, name, year_released, director, rating, Movie.ENT_TYPE)
        Movie._validate_input("Movie length", length)
        Movie._validate_float("Movie length", length)
        self.length = length
        self.awards = []

    def add_award(self, award):
        """ Adds an award to a list if it does not already exist """
        Movie._validate_input("Award", award)
        Movie._validate_string("Award", award)
        if award not in self.awards:
            self.awards.append(award)

    def get_details(self):
        """ Returns the details of movie """
        if not self.awards:
            awards = "None"
        else:
            awards = ", ".join(self.awards)
        return "ID: {}\nType: {}\nName: {}\nGenre: {}\nYear: {}\nDirector: {}\nRating: {}\nLength: {}\nAwards: {}"\
            .format(self.id, self.type, self.name, self.genre_list, self.year_released, self.director, self.rating, self.length, awards)

    def to_dict(self):
        """ Returns a dictionary for writing to the JSON file"""
        dict = {}
        dict['id'] = self.id
        dict['name'] = self.name
        dict['year_released'] = self.year_released
        dict['director'] = self.director
        dict['rating'] = self.rating
        dict['type'] = self.type
        dict['length'] = self.length

        return dict

    def update(self, new):
        if isinstance(new, Movie):
            self.name = new.name
            self.year_released = new.year_released
            self.director = new.director
            self.rating = new.rating
            self.length = new.length




    @staticmethod
    def _validate_string(display_name, input_value):
        """ Private method to validate the input value is a string type """

        if input_value != str(input_value):
            raise ValueError(display_name + " must be a string type.")

    @staticmethod
    def _validate_int(display_name, input_value):
        """ Private method to validate the input value is a int type """

        if input_value != int(input_value):
            raise ValueError(display_name + " must be a integer type.")

    @staticmethod
    def _validate_float(display_name, input_value):
        """ Private method to validate the input value is a int type """

        if input_value != float(input_value):
            raise ValueError(display_name + " must be a float type.")

    @staticmethod
    def _validate_input(display_name, input_value):
        """ Private helper to validate input values as not None or an empty string """
        if input_value is None:
            raise ValueError(display_name + " cannot be undefined.")

        if input_value == "":
            raise ValueError(display_name + " cannot be empty.")

