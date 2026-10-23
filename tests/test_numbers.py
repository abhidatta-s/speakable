"""Tests for numbers.py."""

import unittest

from speakable.numbers import int_to_words, number_to_words, ordinal_words


class IntToWordsTests(unittest.TestCase):
    def check(self, number, expected):
        self.assertEqual(int_to_words(number), expected)

    def test_zero(self):
        self.check(0, "zero")

    def test_ten(self):
        self.check(10, "ten")

    def test_eleven(self):
        self.check(11, "eleven")

    def test_nineteen(self):
        self.check(19, "nineteen")

    def test_twenty(self):
        self.check(20, "twenty")

    def test_twenty_one(self):
        self.check(21, "twenty one")

    def test_hundred(self):
        self.check(100, "one hundred")

    def test_101(self):
        self.check(101, "one hundred one")

    def test_110(self):
        self.check(110, "one hundred ten")

    def test_999(self):
        self.check(999, "nine hundred ninety nine")

    def test_thousand(self):
        self.check(1000, "one thousand")

    def test_1001(self):
        self.check(1001, "one thousand one")

    def test_hundred_thousand(self):
        self.check(100000, "one hundred thousand")

    def test_million(self):
        self.check(1000000, "one million")

    def test_big_mixed(self):
        self.check(
            1234567890,
            "one billion two hundred thirty four million "
            "five hundred sixty seven thousand eight hundred ninety",
        )

    def test_max_supported(self):
        self.check(
            999999999999,
            "nine hundred ninety nine billion nine hundred ninety nine million "
            "nine hundred ninety nine thousand nine hundred ninety nine",
        )

    def test_beyond_range_raises(self):
        with self.assertRaises(ValueError) as context:
            int_to_words(1000000000000)
        self.assertIn("too large", str(context.exception))

    def test_negative(self):
        self.check(-5, "minus five")

    def test_bad_system_raises(self):
        with self.assertRaises(ValueError):
            int_to_words(5, "martian")


class IndianSystemTests(unittest.TestCase):
    def test_lakh(self):
        self.assertEqual(int_to_words(100000, "indian"), "one lakh")

    def test_crore(self):
        self.assertEqual(int_to_words(10000000, "indian"), "one crore")

    def test_mixed(self):
        self.assertEqual(
            int_to_words(12345678, "indian"),
            "one crore twenty three lakh forty five thousand six hundred seventy eight",
        )

    def test_large_crore_chunk(self):
        self.assertEqual(int_to_words(50000000000, "indian"), "five thousand crore")

    def test_small_numbers_same_as_international(self):
        self.assertEqual(int_to_words(999, "indian"), int_to_words(999))

    def test_max_supported_indian(self):
        text = int_to_words(999999999999, "indian")
        self.assertTrue(text.startswith("ninety nine thousand nine hundred ninety nine crore"))

    def test_beyond_range_raises_indian(self):
        with self.assertRaises(ValueError):
            int_to_words(1000000000000, "indian")


class NumberToWordsTests(unittest.TestCase):
    def test_comma_grouped(self):
        self.assertEqual(number_to_words("1,250"), "one thousand two hundred fifty")

    def test_decimal(self):
        self.assertEqual(number_to_words("3.14"), "three point one four")

    def test_negative_decimal(self):
        self.assertEqual(number_to_words("-0.5"), "minus zero point five")

    def test_leading_point(self):
        self.assertEqual(number_to_words(".5"), "zero point five")

    def test_trailing_zero_decimal(self):
        self.assertEqual(number_to_words("2.50"), "two point five zero")

    def test_not_a_number(self):
        with self.assertRaises(ValueError):
            number_to_words("abc")

    def test_indian_option(self):
        self.assertEqual(number_to_words("2,50,000", "indian"), "two lakh fifty thousand")


class OrdinalTests(unittest.TestCase):
    def check(self, text, expected):
        self.assertEqual(ordinal_words(text), expected)

    def test_1st(self):
        self.check("1st", "first")

    def test_2nd(self):
        self.check("2nd", "second")

    def test_3rd(self):
        self.check("3rd", "third")

    def test_4th(self):
        self.check("4th", "fourth")

    def test_11th(self):
        self.check("11th", "eleventh")

    def test_12th(self):
        self.check("12th", "twelfth")

    def test_13th(self):
        self.check("13th", "thirteenth")

    def test_21st(self):
        self.check("21st", "twenty first")

    def test_22nd(self):
        self.check("22nd", "twenty second")

    def test_20th(self):
        self.check(20, "twentieth")

    def test_101st(self):
        self.check("101st", "one hundred first")

    def test_111th(self):
        self.check("111th", "one hundred eleventh")

    def test_100th(self):
        self.check(100, "one hundredth")

    def test_8th_and_9th(self):
        self.check(8, "eighth")
        self.check(9, "ninth")

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            ordinal_words("first")


if __name__ == "__main__":
    unittest.main()
