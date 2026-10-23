"""Tests for normalizer.py and the command line."""

import io
import unittest
from contextlib import redirect_stdout

from speakable.cli import main
from speakable.normalizer import STEPS, explain, normalize, step_numbers, step_percents


class FullSentenceTests(unittest.TestCase):
    def test_spec_example(self):
        self.assertEqual(
            normalize("On 5 Jan 2026 at 9:30 am, Dr. Rao paid Rs. 1,250.50 for the 3rd ticket."),
            "On the fifth of January twenty twenty six at nine thirty a m, Doctor Rao paid "
            "one thousand two hundred fifty rupees and fifty paise for the third ticket.",
        )

    def test_dollars_and_percent(self):
        self.assertEqual(
            normalize("Save $5 with 20% off."),
            "Save five dollars with twenty percent off.",
        )

    def test_distance_and_time(self):
        self.assertEqual(
            normalize("Mr. Shah ran 5 km at 21:05."),
            "Mister Shah ran five kilometers at twenty one oh five.",
        )

    def test_ordinal_in_sentence(self):
        self.assertEqual(normalize("She came 1st and he came 22nd."), "She came first and he came twenty second.")

    def test_iso_date_sentence(self):
        self.assertEqual(
            normalize("Deadline 2026-01-05 at 12:00 pm."),
            "Deadline the fifth of January twenty twenty six at twelve o'clock p m.",
        )

    def test_indian_system(self):
        self.assertEqual(
            normalize("Rs. 1,25,00,000", system="indian"),
            "one crore twenty five lakh rupees",
        )


class NewRuleTests(unittest.TestCase):
    def test_yearless_date_in_sentence(self):
        self.assertEqual(
            normalize("Back on 22nd Oct at 9:30 am."),
            "Back on the twenty second of October at nine thirty a m.",
        )

    def test_month_first_with_year(self):
        self.assertEqual(
            normalize("Oct 22, 2026 is a Thursday"),
            "the twenty second of October twenty twenty six is a Thursday",
        )

    def test_invalid_pm_in_sentence(self):
        self.assertEqual(normalize("Meet at 13:00 pm."), "Meet at thirteen o'clock.")

    def test_year_after_in(self):
        self.assertEqual(normalize("It began in 2025."), "It began in twenty twenty five.")

    def test_year_after_vs(self):
        self.assertEqual(
            normalize("2024 vs. 2025 sales"),
            "two thousand twenty four versus twenty twenty five sales",
        )

    def test_plain_number_after_in_outside_range(self):
        self.assertEqual(normalize("in 2500 cases"), "in two thousand five hundred cases")

    def test_number_not_after_year_word_stays_a_number(self):
        self.assertEqual(normalize("we sold 2025 units"), "we sold two thousand twenty five units")


class NumberStepTests(unittest.TestCase):
    def test_plain_number(self):
        self.assertEqual(normalize("I have 42 apples"), "I have forty two apples")

    def test_decimal(self):
        self.assertEqual(normalize("pi is 3.14"), "pi is three point one four")

    def test_negative(self):
        self.assertEqual(normalize("it is -5 outside"), "it is minus five outside")

    def test_range_is_not_negative(self):
        self.assertEqual(normalize("pages 5-10"), "pages five-ten")

    def test_comma_list_stays_a_list(self):
        self.assertEqual(normalize("1,2,3"), "one,two,three")

    def test_too_big_read_digit_by_digit(self):
        self.assertEqual(step_numbers("1234567890123", "international"), "one two three four five six seven eight nine zero one two three")

    def test_text_without_numbers_unchanged(self):
        self.assertEqual(normalize("hello world"), "hello world")

    def test_empty_text(self):
        self.assertEqual(normalize(""), "")


class StepTests(unittest.TestCase):
    def test_percent_step_keeps_digits(self):
        self.assertEqual(step_percents("50%", "international"), "50 percent")

    def test_step_order(self):
        names = []
        for name, step in STEPS:
            names.append(name)
        self.assertEqual(
            names,
            [
                "money", "dates", "times", "years", "ordinals",
                "percents", "abbreviations", "numbers",
            ],
        )

    def test_explain_returns_one_row_per_step(self):
        rows = explain("Rs. 5")
        self.assertEqual(len(rows), len(STEPS))
        self.assertEqual(rows[0], ("money", "Rs. 5", "five rupees"))

    def test_explain_last_after_equals_normalize(self):
        text = "Dr. Rao at 9:30 am"
        self.assertEqual(explain(text)[-1][2], normalize(text))


class CliTests(unittest.TestCase):
    def run_cli(self, argv):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(argv)
        return code, buffer.getvalue()

    def test_plain(self):
        code, output = self.run_cli(["Rs. 5"])
        self.assertEqual(code, 0)
        self.assertEqual(output, "five rupees\n")

    def test_explain_flag(self):
        code, output = self.run_cli(["--explain", "Rs. 5"])
        self.assertEqual(code, 0)
        self.assertIn("[money]", output)
        self.assertIn("before: Rs. 5", output)
        self.assertIn("Final: five rupees", output)

    def test_indian_flag(self):
        code, output = self.run_cli(["--system", "indian", "100000"])
        self.assertEqual(output, "one lakh\n")


if __name__ == "__main__":
    unittest.main()
