import unittest

from util.nlg import generate_description_of_filter


class TestNLG(unittest.TestCase):

    def test_demonym(self):
        self.assertEqual("Nigerian women surveyed who mentioned EQUALITY",
                         generate_description_of_filter(["Nigeria"], ["EQUALITY"], None, None, "", "",100))

    def test_nothing(self):
        self.assertEqual("All women", generate_description_of_filter([], [], None, None, "", "",10))

    def test_age(self):
        self.assertEqual("Indian and Ugandan women aged 39-41",
                         generate_description_of_filter(["India", "Uganda"], [], 39, 41, "", "",10))

    def test_join_list_1(self):
        self.assertEqual("Women surveyed who mentioned A or B and \"C\"",
                         generate_description_of_filter([], ["A", "B"], None, None, "C", "",10))

    def test_join_list_2(self):
        self.assertEqual("Women surveyed who mentioned \"C\"",
                         generate_description_of_filter([], [], None, None, "C", "",10))

    def test_join_list_3(self):
        self.assertEqual("Women surveyed who mentioned A or B",
                         generate_description_of_filter([], ["A", "B"], None, None, "", "",10))
    
    def test_singular(self):
        self.assertEqual("Woman who mentioned A or B",
                         generate_description_of_filter([], ["A", "B"], None, None, "", "", 1))