"""Tests for money.py."""

import unittest

from speakable.money import convert_money


class InrTests(unittest.TestCase):
    def test_rs_dot_with_decimals(self):
        self.assertEqual(
            convert_money("Rs. 1,250.50"),
            "one thousand two hundred fifty rupees and fifty paise",
        )

    def test_rs_no_dot(self):
        self.assertEqual(convert_money("Rs 20"), "twenty rupees")

    def test_rupee_symbol(self):
        self.assertEqual(convert_money("₹100"), "one hundred rupees")

    def test_inr_code(self):
        self.assertEqual(convert_money("INR 75"), "seventy five rupees")

    def test_singular_rupee(self):
        self.assertEqual(convert_money("Rs. 1"), "one rupee")

    def test_singular_paisa(self):
        self.assertEqual(convert_money("Rs. 5.01"), "five rupees and one paisa")

    def test_only_paise(self):
        self.assertEqual(convert_money("₹0.50"), "fifty paise")

    def test_indian_grouping(self):
        self.assertEqual(
            convert_money("Rs. 1,25,000", "indian"), "one lakh twenty five thousand rupees"
        )


class UsdTests(unittest.TestCase):
    def test_dollar_sign(self):
        self.assertEqual(convert_money("$5"), "five dollars")

    def test_usd_code(self):
        self.assertEqual(convert_money("USD 12.25"), "twelve dollars and twenty five cents")

    def test_singular_dollar(self):
        self.assertEqual(convert_money("$1"), "one dollar")

    def test_singular_cent(self):
        self.assertEqual(convert_money("$0.01"), "one cent")

    def test_dollar_and_cent_singular(self):
        self.assertEqual(convert_money("$1.01"), "one dollar and one cent")

    def test_single_decimal_digit_means_tens(self):
        self.assertEqual(convert_money("$1.5"), "one dollar and fifty cents")

    def test_zero_dollars(self):
        self.assertEqual(convert_money("$0"), "zero dollars")

    def test_extra_decimals_are_cut(self):
        self.assertEqual(convert_money("$2.999"), "two dollars and ninety nine cents")

    def test_big_amount(self):
        self.assertEqual(convert_money("$1,000,000"), "one million dollars")


class EdgeCaseTests(unittest.TestCase):
    def test_inside_sentence(self):
        self.assertEqual(convert_money("It costs $5. Fine."), "It costs five dollars. Fine.")

    def test_letters_before_rs_are_ignored(self):
        self.assertEqual(convert_money("cars 5"), "cars 5")

    def test_too_large_left_alone(self):
        self.assertEqual(convert_money("$9,999,999,999,999"), "$9,999,999,999,999")

    def test_no_money(self):
        self.assertEqual(convert_money("hello 5"), "hello 5")


if __name__ == "__main__":
    unittest.main()
