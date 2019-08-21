import unittest
from unittest import TestCase
from streaming_service import StreamingService
from movie import Movie
from tv_series import TVSeries
import inspect
from sqlalchemy import create_engine
from base import Base
import os

class TestStreamingService(TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///test_streaming_service.sqlite')

        Base.metadata.create_all(engine)
        Base.metadata.bind = engine

        self.service_mgr = StreamingService('test_streaming_service.sqlite')

        self.logPoint()

    def test_add_arg(self):
        """ T02 Test add for raising the error when the arguments are none or empty strings"""
        self.assertRaisesRegex(ValueError, 'Movie or TV series cannot be undefined.', self.service_mgr.add, None)

    def test_get_arg(self):
        """ T03 Test get for raising the error when the argument is none or not integer"""
        self.assertRaisesRegex(ValueError, 'ID must be a integer type.', self.service_mgr.get, "1")

    def test_get_all_by_type_arg(self):
        """ T04 Test get_all_by_type for raising the error when the arguments are none or empty strings"""
        self.assertRaisesRegex(ValueError, 'Type must be a string type.', self.service_mgr.get_all_by_type, 1)

    def test_update_arg(self):
        """ T05 Test update for raising the error when the argument is none"""
        self.assertRaisesRegex(ValueError, 'Movie or TV series cannot be undefined.', self.service_mgr.update, None)

    def test_delete_arg(self):
        """ T06 Test delete for raising the error when the argument is none or not integer"""
        self.assertRaisesRegex(ValueError, 'ID must be a integer type.', self.service_mgr.delete, "1")

    def test_add(self):
        """ T07 Test add for adding the object"""
        test_m = Movie(111, "The Hateful Eight", 2015, "Quentin", 7.8, 'Movie', 3.7)
        test_t = TVSeries(222, "Breaking Bad", 2008, "Michelle", 9.5, 'TV series')
        id_test_m = self.service_mgr.add(test_m)
        id_test_t = self.service_mgr.add(test_t)
        self.assertEqual(len(self.service_mgr.get_all()), 2)
        self.assertEqual(id_test_m == 111 and id_test_t == 222, True)
        self.service_mgr.delete(111)
        self.service_mgr.delete(222)

    def test_get(self):
        """ T08 Test get for getting the right object"""
        test_m = Movie(777, "The Hateful Eight", 2015, "Quentin", 7.8, 'Movie', 3.7)
        id_test_m = self.service_mgr.add(test_m)
        self.assertEqual(self.service_mgr.get(id_test_m).name, "The Hateful Eight")

    def test_get_all(self):
        """ T09 Test get for getting a list of all objects"""
        test_m = Movie(333, "The Hateful Eight", 2015, "Quentin", 7.8, 'Movie', 3.7)
        test_t = TVSeries(444, "Breaking Bad", 2008, "Michelle", 9.5, 'TV series')
        id_test_m = self.service_mgr.add(test_m)
        id_test_t = self.service_mgr.add(test_t)
        self.assertEqual(len(self.service_mgr.get_all()), 2)

    def test_get_all_by_type(self):
        """ T10 Test the return value of get_all_by_type"""
        test_m = Movie(555, "The Hateful Eight", 2015, "Quentin", 7.8, 'Movie', 3.7)
        test_t = TVSeries(666, "Breaking Bad", 2008, "Michelle", 9.5, 'TV series')
        id_test_m = self.service_mgr.add(test_m)
        id_test_t = self.service_mgr.add(test_t)
        self.assertEqual(self.service_mgr.get_all_by_type('Movie')[0].type, 'Movie')

    def test_update(self):
        """ T11 Test update for updating the right object"""
        test_m = Movie(777, "The Hateful Eight", 2015, "Quentin", 7.8, 'Movie', 3.7)
        id_test_m = self.service_mgr.add(test_m)
        m2 = Movie(777, "Forrest Gump", 1994, "Robert", 9.0, 'Movie', 2)
        self.service_mgr.update(m2)
        self.assertEqual(self.service_mgr.get(id_test_m).rating, 9.0)

    def test_delete(self):
        """ T12 Test delete for deleting the right object"""
        m3 = Movie(3, "The Avengers", 2012, "Joss", 8.1, 'Movie', 2.23)
        id = self.service_mgr.add(m3)
        self.service_mgr.delete(id)
        self.assertRaisesRegex(ValueError, 'ID not found', self.service_mgr.get, 3)

    def logPoint(self):
        """ Utility function used for module functions and class methods """
        current_test = self.id().split('.')[-1]
        calling_function = inspect.stack()[1][3]
        print('in %s - %s()' % (current_test, calling_function))

    def tearDown(self):
        """ Prints a log point when test is finished """
        self.logPoint()
        os.remove('test_streaming_service.sqlite')

if __name__ == "__main__":
    unittest.main()