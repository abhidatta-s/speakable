"""Tests for abbreviations.py."""

import unittest

from speakable.abbreviations import expand_abbreviations


class AbbreviationTests(unittest.TestCase):
    def check(self, text, expected):
        self.assertEqual(expand_abbreviations(text), expected)

    def test_doctor(self):
        self.check("Dr. Rao", "Doctor Rao")

    def test_mister(self):
        self.check("Mr. Shah", "Mister Shah")

    def test_missus(self):
        self.check("Mrs. Shah", "Missus Shah")

    def test_miss(self):
        self.check("Ms. Iyer", "Miss Iyer")

    def test_street(self):
        self.check("MG St.", "MG Street")

    def test_versus(self):
        self.check("India vs. Japan", "India versus Japan")

    def test_for_example(self):
        self.check("fruit, e.g. apples", "fruit, for example apples")

    def test_that_is(self):
        self.check("one, i.e. single", "one, that is single")

    def test_etc(self):
        self.check("pens, etc. are here", "pens, et cetera are here")

    def test_km(self):
        self.check("5 km", "5 kilometers")

    def test_kg(self):
        self.check("2kg", "2kilograms")

    def test_percent_sign(self):
        self.check("% change", "percent change")

    def test_not_inside_a_word(self):
        self.check("kmh", "kmh")

    def test_not_in_the_middle_of_a_word(self):
        self.check("Mst. here", "Mst. here")

    def test_case_sensitive(self):
        self.check("dr. who", "dr. who")

    def test_no_abbreviations(self):
        self.check("plain words", "plain words")


if __name__ == "__main__":
    unittest.main()
