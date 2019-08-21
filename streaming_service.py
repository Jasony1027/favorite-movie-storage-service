from movie import Movie
from tv_series import TVSeries
from abstract_entertainment import AbstractEntertainment
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base


class StreamingService:
    """ Streaming Service Class - Maintains the details of each service """
    def __init__(self, db_filename):
        """ Constructor - Initializes the main attributes for the streaming service """
        if db_filename is None or db_filename == "":
            raise ValueError("Invalid Database File")

        engine = create_engine('sqlite:///' + db_filename)
        Base.metadata.bind = engine
        self._db_session = sessionmaker(bind=engine)

    def add(self, ent):
        """ Method that adds a movie or tv series to the list """
        StreamingService._validate_input("Movie or TV series", ent)
        session = self._db_session()
        ent_list = self.get_all()
        for e in ent_list:
            if e.id == ent.id:
                session.close()
                raise ValueError('ID already exist')
        session.add(ent)
        session.commit()
        ent_id = ent.id
        session.close()

        return ent_id

    def get(self, id):
        """ Returns a movie or tv series based on ID """
        StreamingService._validate_int("ID", id)
        session = self._db_session()
        abs_ent = session.query(AbstractEntertainment).filter(AbstractEntertainment.id == id).first()
        if abs_ent is None:
            session.close()
            raise ValueError("ID not found")

        if abs_ent.type == 'Movie':
            existing_ent = session.query(Movie).filter(Movie.id == id).first()
        else:
            existing_ent = session.query(TVSeries).filter(TVSeries.id == id).first()

        session.close()

        return existing_ent

    def get_all(self):
        """ Returns all the movies or tv series in the list """
        session = self._db_session()
        movies = session.query(Movie).filter(Movie.type == 'Movie').all()
        tv_series = session.query(TVSeries).filter(TVSeries.type == 'TV series').all()
        session.close()

        existing_ents = movies + tv_series

        return existing_ents

    def get_all_by_type(self, ent_type):
        """ Returns a list movies or tv series based on type """
        StreamingService._validate_string("Type", ent_type)
        if ent_type != 'Movie' and ent_type != 'TV series':
            raise ValueError("Invalid entertainment type")

        session = self._db_session()

        if ent_type == "Movie":
            type_list = session.query(Movie).filter(Movie.type == 'Movie').all()
        else:
            type_list = session.query(TVSeries).filter(TVSeries.type == 'TV series').all()

        session.close()

        return type_list
        
    def update(self, ent):
        """ Updates a movie or tv series """
        StreamingService._validate_input("Movie or TV series", ent)

        session = self._db_session()

        if ent.type == 'Movie':
            existing_ent = session.query(Movie).filter(Movie.id == ent.id).first()
        else:
            existing_ent = session.query(TVSeries).filter(TVSeries.id == ent.id).first()

        ents = self.get_all()
        for e in ents:
            if e.name == ent.name and e.id != existing_ent.id:
                session.close()
                raise ValueError("ID not found")

        existing_ent.update(ent)

        session.commit()
        session.close()

    def delete(self, id):
        """ Deletes a movie or tv series based on ID """
        StreamingService._validate_int("ID", id)
        session = self._db_session()
        existing_ent = session.query(AbstractEntertainment).filter(AbstractEntertainment.id == id).first()
        if existing_ent is None:
            session.close()
            raise ValueError("ID not found")

        session.delete(existing_ent)
        session.commit()
        session.close()

    @staticmethod
    def _validate_string(display_name, input_value):
        """ Private method to validate the input value is a string type """

        if input_value != str(input_value):
            raise ValueError(display_name + " must be a string type.")

    @staticmethod
    def _validate_int(display_name, input_value):
        """ Private method to validate the input value is a int type """

        if type(input_value) is not int:
            raise ValueError(display_name + " must be a integer type.")

    @staticmethod
    def _validate_float(display_name, input_value):
        """ Private method to validate the input value is a float type """

        if input_value != float(input_value):
            raise ValueError(display_name, " must be a float type.")

    @staticmethod
    def _validate_input(display_name, input_value):
        """ Private helper to validate input values as not None or an empty string """

        if input_value is None or not isinstance(input_value, AbstractEntertainment):
            raise ValueError(display_name + " cannot be undefined.")

        if input_value == "":
            raise ValueError(display_name + " cannot be empty.")




