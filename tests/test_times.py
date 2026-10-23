"""Tests for times.py."""

import unittest

from speakable.times import convert_times


class TwelveHourTests(unittest.TestCase):
    def test_am(self):
        self.assertEqual(convert_times("9:30 am"), "nine thirty a m")

    def test_pm(self):
        self.assertEqual(convert_times("4:45 pm"), "four forty five p m")

    def test_on_the_hour(self):
        self.assertEqual(convert_times("9:00 am"), "nine o'clock a m")

    def test_noon_style(self):
        self.assertEqual(convert_times("12:00 pm"), "twelve o'clock p m")

    def test_oh_minutes(self):
        self.assertEqual(convert_times("9:05 am"), "nine oh five a m")

    def test_no_minutes(self):
        self.assertEqual(convert_times("9 pm"), "nine p m")

    def test_upper_case(self):
        self.assertEqual(convert_times("9:30 AM"), "nine thirty a m")

    def test_dotted(self):
        self.assertEqual(convert_times("9:30 a.m. sharp"), "nine thirty a m sharp")

    def test_no_space(self):
        self.assertEqual(convert_times("7:15pm"), "seven fifteen p m")

    def test_hour_13_with_pm_drops_the_pm(self):
        # 13 is not a valid 12 hour clock hour, so the pm is dropped (24 hour reading).
        self.assertEqual(convert_times("13:00 pm"), "thirteen o'clock")

    def test_invalid_12_hour_with_minutes(self):
        self.assertEqual(convert_times("15:30 pm"), "fifteen thirty")

    def test_invalid_12_hour_oh_minutes(self):
        self.assertEqual(convert_times("21:05 PM"), "twenty one oh five")

    def test_invalid_12_hour_without_minutes(self):
        self.assertEqual(convert_times("13 pm"), "thirteen")

    def test_hour_zero_with_am(self):
        self.assertEqual(convert_times("0:30 am"), "zero thirty")

    def test_invalid_12_hour_dotted(self):
        self.assertEqual(convert_times("14:00 p.m. sharp"), "fourteen o'clock sharp")

    def test_impossible_time_with_pm_left_alone(self):
        self.assertEqual(convert_times("25:00 pm"), "25:00 pm")

    def test_never_o_clock_pm(self):
        self.assertNotIn("o'clock p", convert_times("13:00 pm"))


class TwentyFourHourTests(unittest.TestCase):
    def test_with_minutes(self):
        self.assertEqual(convert_times("21:05"), "twenty one oh five")

    def test_on_the_hour(self):
        self.assertEqual(convert_times("21:00"), "twenty one o'clock")

    def test_midnight_half(self):
        self.assertEqual(convert_times("00:30"), "zero thirty")

    def test_in_sentence(self):
        self.assertEqual(convert_times("Train at 18:45 today"), "Train at eighteen forty five today")

    def test_invalid_hour(self):
        self.assertEqual(convert_times("25:00"), "25:00")

    def test_invalid_minute(self):
        self.assertEqual(convert_times("10:75"), "10:75")


class NotATimeTests(unittest.TestCase):
    def test_word_starting_with_am(self):
        self.assertEqual(convert_times("5 amazing things"), "5 amazing things")

    def test_plain_number(self):
        self.assertEqual(convert_times("I have 9 cats"), "I have 9 cats")


if __name__ == "__main__":
    unittest.main()
