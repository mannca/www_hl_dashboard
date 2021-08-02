import unittest

from util.nlg import generate_age_description


class TestAgeRange(unittest.TestCase):

    def test_lower_and_upper_age_bounds(self):
        self.assertEqual(" aged 32-38", generate_age_description(32, 38))

    def test_lower_age_only(self):
        self.assertEqual(" aged 18 and up", generate_age_description(18, None))

    def test_upper_age_only(self):
        self.assertEqual(" aged 38 and under", generate_age_description(None, 38))