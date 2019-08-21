from sqlalchemy import Column, Integer, String, Float
from abstract_entertainment import AbstractEntertainment
from datetime import datetime


class TVSeries(AbstractEntertainment):
    """ TV Series Class - Maintains the details of each TV series """
    ENT_TYPE = 'TV series'

    def __init__(self, id, name, year_released, director, rating, type):
        """ Constructor - Initializes the main attributes of each TV series """
        super().__init__(id, name, year_released, director, rating, TVSeries.ENT_TYPE)
        self.seasons = []
        self.released_end_dates = []

    def get_episode(self, episode_name):
        """ Returns each episode in season """
        TVSeries._validate_input("Episode name", episode_name)
        for season in self.seasons:
            if episode_name in season:
                return "S{}:E{}".format(self.seasons.index(season)+1, season.index(episode_name)+1)

    def is_ended(self):
        """ Returns True if tv series is ended """
        return len(self.released_end_dates) == 2

    def get_time_period(self):
        """ Returns the release and end dates if ended, else returns a string """
        if self.is_ended():
            return str((self.released_end_dates[1] - self.released_end_dates[0]).days) + " days"
        else:
            return "Ongoing TV series"

    def add_date(self, date):
        """ Adds date to tv series if not ended """
        if len(self.released_end_dates) == 2:
            return
        TVSeries._validate_datetime_input("Date", date)
        if self.released_end_dates and date < self.released_end_dates[0]:
            raise ValueError("End date cannot be less than start date")
        else:
            self.released_end_dates.append(date)

    def add_season(self, season=None):
        """ Adds a season to a tv series """
        if season is None:
            season = []
        if season not in self.seasons:
            self.seasons.append(season)

    def add_episode(self, episode_name, season_num=None):
        """ Adds an episode to a season """
        if season_num is None:
            season_num = len(self.seasons)
        elif season_num>len(self.seasons):
            raise ValueError('Don\'t rush')
        ep = len(self.seasons[season_num - 1]) + 1
        self.seasons[season_num - 1].append(episode_name)

    def update_episode(self, episode_num, season_num, episode_name):
        """ Updates episode """
        self.seasons[season_num-1][episode_num-1] = episode_name

    def get_details(self):
        """ Returns the details of tv series """
        season_output = ""
        counter = 1
        for season in self.seasons:
            season_output += "S"+str(counter)+" " + ", ".join(season)+"\n"
            counter += 1

        return "ID: {}\nType: {}\nName: {}\nGenre: {}\nYear: {}\nDirector: {}\nActors: {}\nRating: {}\nSeasons: {}"\
            .format(self.id, self.type, self.name, self.genre_list, self.year_released, self.director, self.actors, self.rating, season_output)

    def to_dict(self):
        """ Returns a dictionary for writing to the JSON file"""
        dict = {}
        dict['id'] = self.id
        dict['name'] = self.name
        dict['year_released'] = self.year_released
        dict['director'] = self.director
        dict['rating'] = self.rating
        dict['type'] = self.type
        return dict

    def update(self, new):
        if isinstance(new, TVSeries):
            self.name = new.name
            self.year_released = new.year_released
            self.director = new.director
            self.rating = new.rating

    @staticmethod
    def _validate_datetime_input(display_name, input_value):
        """ Private helper to validate input values as not None or an empty string """

        if input_value is None:
            raise ValueError(display_name + " cannot be undefined.")

        if input_value == "":
            raise ValueError(display_name + " cannot be empty.")

        if type(input_value) is not datetime:
            raise ValueError(display_name + " must be a datetime type.")

