"""Tests for dates.py."""

import unittest

from speakable.dates import convert_bare_years, convert_dates, year_to_words


class YearTests(unittest.TestCase):
    def test_2026(self):
        self.assertEqual(year_to_words(2026), "twenty twenty six")

    def test_2000(self):
        self.assertEqual(year_to_words(2000), "two thousand")

    def test_2005(self):
        self.assertEqual(year_to_words(2005), "two thousand five")

    def test_1999(self):
        self.assertEqual(year_to_words(1999), "nineteen ninety nine")

    def test_1905(self):
        self.assertEqual(year_to_words(1905), "nineteen oh five")

    def test_1900(self):
        self.assertEqual(year_to_words(1900), "nineteen hundred")

    def test_2010(self):
        self.assertEqual(year_to_words(2010), "twenty ten")


class DateFormatTests(unittest.TestCase):
    EXPECTED = "the fifth of January twenty twenty six"

    def test_day_month_year(self):
        self.assertEqual(convert_dates("5 Jan 2026"), self.EXPECTED)

    def test_day_with_ordinal_suffix(self):
        self.assertEqual(convert_dates("5th January 2026"), self.EXPECTED)

    def test_month_day_year(self):
        self.assertEqual(convert_dates("January 5, 2026"), self.EXPECTED)

    def test_iso(self):
        self.assertEqual(convert_dates("2026-01-05"), self.EXPECTED)

    def test_slash_is_day_first(self):
        self.assertEqual(convert_dates("05/01/2026"), self.EXPECTED)

    def test_slash_day_first_not_us_style(self):
        self.assertEqual(
            convert_dates("01/05/2026"), "the first of May twenty twenty six"
        )

    def test_lower_case_month(self):
        self.assertEqual(convert_dates("5 jan 2026"), self.EXPECTED)

    def test_dot_after_month(self):
        self.assertEqual(convert_dates("5 Jan. 2026"), self.EXPECTED)

    def test_sept_spelling(self):
        self.assertEqual(
            convert_dates("22 Sept 1999"), "the twenty second of September nineteen ninety nine"
        )


class InvalidDateTests(unittest.TestCase):
    def test_no_such_day(self):
        self.assertEqual(convert_dates("31/02/2026"), "31/02/2026")

    def test_month_13(self):
        self.assertEqual(convert_dates("2026-13-01"), "2026-13-01")

    def test_leap_day_valid(self):
        self.assertEqual(
            convert_dates("29 Feb 2024"), "the twenty ninth of February twenty twenty four"
        )

    def test_leap_day_invalid(self):
        self.assertEqual(convert_dates("29 Feb 2025"), "29 Feb 2025")

    def test_text_around_date(self):
        self.assertEqual(
            convert_dates("Due on 2026-01-05, ok?"),
            "Due on the fifth of January twenty twenty six, ok?",
        )


class YearlessDateTests(unittest.TestCase):
    def test_ordinal_day_and_month(self):
        self.assertEqual(convert_dates("22nd Oct"), "the twenty second of October")

    def test_plain_day_and_month(self):
        self.assertEqual(convert_dates("5 Jan"), "the fifth of January")

    def test_month_first(self):
        self.assertEqual(convert_dates("Oct 22"), "the twenty second of October")

    def test_month_first_with_ordinal(self):
        self.assertEqual(convert_dates("Oct 22nd"), "the twenty second of October")

    def test_month_first_with_year_and_comma(self):
        self.assertEqual(
            convert_dates("Oct 22, 2026"), "the twenty second of October twenty twenty six"
        )

    def test_abbreviation_with_dot_day_first(self):
        self.assertEqual(convert_dates("22 Oct. is near"), "the twenty second of October is near")

    def test_abbreviation_with_dot_month_first(self):
        self.assertEqual(convert_dates("Oct. 22 is near"), "the twenty second of October is near")

    def test_full_month_name(self):
        self.assertEqual(convert_dates("3rd March"), "the third of March")

    def test_in_a_sentence(self):
        self.assertEqual(
            convert_dates("See you on 5 Jan, ok?"), "See you on the fifth of January, ok?"
        )

    def test_impossible_day_left_alone(self):
        self.assertEqual(convert_dates("31 Feb"), "31 Feb")

    def test_leap_day_without_year(self):
        self.assertEqual(convert_dates("Feb 29"), "the twenty ninth of February")

    def test_word_that_only_starts_like_a_month(self):
        self.assertEqual(convert_dates("5 Marathon runners"), "5 Marathon runners")

    def test_invalid_full_date_not_half_converted(self):
        self.assertEqual(convert_dates("29 Feb 2025"), "29 Feb 2025")

    def test_month_then_time_is_not_a_date(self):
        self.assertEqual(convert_dates("Oct 22:30"), "Oct 22:30")

    def test_month_then_year_only_is_not_a_date(self):
        self.assertEqual(convert_dates("Oct 2026"), "Oct 2026")


class BareYearTests(unittest.TestCase):
    def test_in(self):
        self.assertEqual(convert_bare_years("in 2025"), "in twenty twenty five")

    def test_since(self):
        self.assertEqual(convert_bare_years("since 1999"), "since nineteen ninety nine")

    def test_vs_dot(self):
        self.assertEqual(convert_bare_years("2024 vs. 2025"), "2024 vs. twenty twenty five")

    def test_versus(self):
        self.assertEqual(convert_bare_years("versus 2000"), "versus two thousand")

    def test_by(self):
        self.assertEqual(convert_bare_years("by 2030"), "by twenty thirty")

    def test_until(self):
        self.assertEqual(convert_bare_years("until 2005"), "until two thousand five")

    def test_from(self):
        self.assertEqual(convert_bare_years("from 1900"), "from nineteen hundred")

    def test_capital_letter_kept(self):
        self.assertEqual(convert_bare_years("In 2025"), "In twenty twenty five")

    def test_out_of_range_left_alone(self):
        self.assertEqual(convert_bare_years("in 2100"), "in 2100")
        self.assertEqual(convert_bare_years("in 1899"), "in 1899")

    def test_other_words_left_alone(self):
        self.assertEqual(convert_bare_years("about 2025"), "about 2025")

    def test_word_ending_in_in_is_ignored(self):
        self.assertEqual(convert_bare_years("again 2025"), "again 2025")

    def test_longer_number_left_alone(self):
        self.assertEqual(convert_bare_years("in 20255"), "in 20255")

    def test_decimal_left_alone(self):
        self.assertEqual(convert_bare_years("in 2025.5"), "in 2025.5")

    def test_only_first_number_after_word(self):
        self.assertEqual(
            convert_bare_years("from 2000 to 2005"), "from two thousand to 2005"
        )


if __name__ == "__main__":
    unittest.main()
