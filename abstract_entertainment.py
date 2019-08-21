from sqlalchemy import Column, Integer, String, Float
from base import Base


class AbstractEntertainment(Base):
    """ Abstract Entertainment Class - Maintains the details of each abstract entertainment """

    __tablename__ = 'entertainment'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    year_released = Column(String(250), nullable=False)
    director = Column(String(100), nullable=False)
    rating = Column(Float(3), nullable=False)
    type = Column(String(10), nullable=False)

    def __init__(self,  id, name, year_released, director, rating, type):
        """ Constructor - Initializes the main attributes for the abstract entertainment """

        AbstractEntertainment._validate_input("ID", id)
        self.id = id
        AbstractEntertainment._validate_input("Name", name)
        self.name = name
        AbstractEntertainment._validate_input("Year released", year_released)
        self.year_released = year_released
        AbstractEntertainment._validate_input("Director", director)
        self.director = director
        AbstractEntertainment._validate_input("Rating", rating)
        self.rating = rating
        self.genre_list = []
        self.actors = []
        self.type = type

    def is_anime(self):
        """ Returns True if genre is anime """
        return 'anime' in self.genre_list


    def add_genre(self, genre):
        """ Adds a genre to the genre list if the genre does not already exist """
        AbstractEntertainment._validate_input("Genre", genre)
        if genre not in self.genre_list:
            self.genre_list.append(genre)

    def add_actor(self, actor):
        """ Adds an actor to the actor list if the actor does not already exists """
        AbstractEntertainment._validate_input("Actor", actor)
        if actor not in self.actors:
            self.actors.append(actor)

    def to_dict(self):
        """ Abstract method for fromatting the object in movie or tv_series or raises implementation error is not defined """
        raise NotImplementedError('Must be implemented')

    def update(self,new):
        """ Abstract method for updating the  movie or tv_series object or raises implementation error is not defined """
        raise NotImplementedError('Must be implemented')

    @staticmethod
    def _validate_input(display_name, input_value):
        """ Private helper to validate input values as not None or an empty string """

        if input_value is None:
            raise ValueError(display_name + " cannot be undefined.")

        if input_value == "":
            raise ValueError(display_name + " cannot be empty.")

