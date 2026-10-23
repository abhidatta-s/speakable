"""Put all the steps together: written text in, spoken text out.

ORDER MATTERS. Each step runs on the output of the one before it:
  1. money          "Rs. 1,250.50" must go first, before its digits become plain numbers
  2. dates          "5 Jan 2026" must go before times and plain numbers
  3. times          "9:30 am" before plain numbers
  4. years          "in 2025" (a bare year after in, since, by ...) before plain numbers
  5. ordinals       "3rd" before plain numbers
  6. percents       "50%" becomes "50 percent" (the 50 is read in the last step)
  7. abbreviations  "Dr." and "km"
  8. numbers        everything left over, like "42" or "3.14"

Every step is a small function taking (text, system) and returning new text,
so each one can be tested and explained on its own.
"""

import re

from speakable.abbreviations import expand_abbreviations
from speakable.dates import convert_bare_years, convert_dates
from speakable.money import convert_money
from speakable.numbers import digits_to_words, number_to_words, ordinal_words
from speakable.times import convert_times

# A number like 42, -7, 1,250 or 3.14. A minus sign counts only when it is not
# glued to a word or digit, so "5-10" is not read as "five minus ten".
NUMBER_PATTERN = re.compile(r"(?:(?<![\w.])-)?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?")
# 1st, 22nd, 101st
ORDINAL_PATTERN = re.compile(r"\b(\d+)(?:st|nd|rd|th)\b", re.IGNORECASE)
# 50% or 50 %
PERCENT_PATTERN = re.compile(r"(\d)\s?%")


def step_money(text, system):
    return convert_money(text, system)


def step_dates(text, system):
    return convert_dates(text)


def step_times(text, system):
    return convert_times(text)


def step_years(text, system):
    return convert_bare_years(text)


def step_ordinals(text, system):
    def replacer(match):
        try:
            return ordinal_words(match.group(1))
        except ValueError:
            return match.group(0)

    return ORDINAL_PATTERN.sub(replacer, text)


def step_percents(text, system):
    # Keep the digit, add the word. The number itself is read in step_numbers.
    return PERCENT_PATTERN.sub(r"\1 percent", text)


def step_abbreviations(text, system):
    return expand_abbreviations(text)


def _read_digits_one_by_one(text):
    """Fallback for numbers too big to read normally, like a long ID."""
    digits = ""
    for ch in text:
        if ch.isdigit():
            digits = digits + ch
    spoken = digits_to_words(digits)
    if text.startswith("-"):
        spoken = "minus " + spoken
    return spoken


def step_numbers(text, system):
    def replacer(match):
        try:
            return number_to_words(match.group(0), system)
        except ValueError:
            return _read_digits_one_by_one(match.group(0))

    return NUMBER_PATTERN.sub(replacer, text)


# The pipeline: (name shown by --explain, function). Order is the order of the list.
STEPS = [
    ("money", step_money),
    ("dates", step_dates),
    ("times", step_times),
    ("years", step_years),
    ("ordinals", step_ordinals),
    ("percents", step_percents),
    ("abbreviations", step_abbreviations),
    ("numbers", step_numbers),
]


def explain(text, system="international"):
    """Run every step and return a list of (step name, before, after)."""
    results = []
    for name, step in STEPS:
        before = text
        text = step(text, system)
        results.append((name, before, text))
    return results


def normalize(text, system="international"):
    """Turn written text into the words a text-to-speech voice should say."""
    for name, step in STEPS:
        text = step(text, system)
    return text
