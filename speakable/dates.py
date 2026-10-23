"""Turn written dates into spoken words.

Supported formats:
  5 Jan 2026, 5th January 2026   (day first)
  January 5, 2026                (month first)
  2026-01-05                     (ISO: year-month-day)
  05/01/2026                     (DD/MM/YYYY, the Indian convention, NOT the US one)
  22nd Oct, 5 Jan, Oct 22        (no year: day and month only)

Every format is spoken the same way: "the fifth of January twenty twenty six"
(or "the fifth of January" when there is no year).
Impossible dates (like 31/02/2026) are left unchanged.
Month abbreviations work with or without a dot ("Oct" or "Oct.").
A dot right after a year-less month ("22 Oct.") is swallowed, even at the end of a sentence.

Bare years: a four digit number from 1900 to 2099 right after in, since, vs., versus,
by, until or from is read as a year ("in 2025" -> "in twenty twenty five").
Only the number right after the word is changed ("from 2000 to 2005" changes just 2000).
"""

import calendar
import re

from speakable.numbers import int_to_words, ordinal_words

MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December",
]

# Every spelling we accept, in lower case, mapped to the month number.
MONTH_NUMBERS = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

# Longest names first, so "september" is tried before "sep".
_MONTH_REGEX = "|".join(sorted(MONTH_NUMBERS, key=len, reverse=True))

# "5 Jan 2026" or "5th January, 2026"
DAY_MONTH_YEAR = re.compile(
    r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(" + _MONTH_REGEX + r")\.?,?\s+(\d{4})\b",
    re.IGNORECASE,
)
# "January 5, 2026" or "Jan 5th 2026"
MONTH_DAY_YEAR = re.compile(
    r"\b(" + _MONTH_REGEX + r")\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})\b",
    re.IGNORECASE,
)
# "22nd Oct", "5 Jan." (no year). \b after the month stops "5 Marathon" matching "mar".
# The lookahead refuses to match when a year follows, so "29 Feb 2025" stays untouched.
DAY_MONTH = re.compile(
    r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(" + _MONTH_REGEX + r")\b\.?(?!,?\s*\d{4})",
    re.IGNORECASE,
)
# "Oct 22", "Oct. 22nd" (no year). The (?!:) stops "Oct 22:30" from matching.
MONTH_DAY = re.compile(
    r"\b(" + _MONTH_REGEX + r")\b\.?\s+(\d{1,2})(?:st|nd|rd|th)?\b(?![:\d])(?!,?\s*\d{4})",
    re.IGNORECASE,
)
# "2026-01-05"
ISO_DATE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
# "05/01/2026" means day 5, month 1
SLASH_DATE = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b")
# "in 2025", "since 1999", "vs. 2020": a word that usually comes before a year,
# then a four digit number from 1900 to 2099. (?![,.]?\d) skips things like "2025.5".
BARE_YEAR = re.compile(
    r"(?<!\w)(in|since|vs\.|versus|by|until|from)(\s+)((?:19|20)\d\d)\b(?![,.]?\d)",
    re.IGNORECASE,
)


def year_to_words(year):
    """Read a four digit year the way people say it.

    2026 -> twenty twenty six, 2000 -> two thousand, 2005 -> two thousand five,
    1999 -> nineteen ninety nine, 1905 -> nineteen oh five, 1900 -> nineteen hundred.
    """
    if year % 1000 == 0:
        return int_to_words(year)
    if 2000 < year < 2010:
        return "two thousand " + int_to_words(year % 100)
    if year % 100 == 0:
        return int_to_words(year // 100) + " hundred"

    first_half = int_to_words(year // 100)
    second = year % 100
    if second < 10:
        return first_half + " oh " + int_to_words(second)
    return first_half + " " + int_to_words(second)


def date_to_words(day, month, year):
    """Return the spoken date, or None if the date does not exist."""
    if month < 1 or month > 12:
        return None
    if day < 1 or day > calendar.monthrange(year, month)[1]:
        return None
    return (
        "the " + ordinal_words(day) + " of " + MONTH_NAMES[month]
        + " " + year_to_words(year)
    )


def date_without_year_to_words(day, month):
    """Return "the fifth of January", or None if the day and month do not exist."""
    if month < 1 or month > 12:
        return None
    # 2024 is a leap year, so 29 Feb is accepted when we do not know the year.
    if day < 1 or day > calendar.monthrange(2024, month)[1]:
        return None
    return "the " + ordinal_words(day) + " of " + MONTH_NAMES[month]


def _finish(match, day, month, year):
    """Use the spoken date if valid, else keep the original text."""
    spoken = date_to_words(day, month, year)
    if spoken is None:
        return match.group(0)
    return spoken


def _day_month_year(match):
    month = MONTH_NUMBERS[match.group(2).lower()]
    return _finish(match, int(match.group(1)), month, int(match.group(3)))


def _month_day_year(match):
    month = MONTH_NUMBERS[match.group(1).lower()]
    return _finish(match, int(match.group(2)), month, int(match.group(3)))


def _day_month(match):
    month = MONTH_NUMBERS[match.group(2).lower()]
    spoken = date_without_year_to_words(int(match.group(1)), month)
    if spoken is None:
        return match.group(0)
    return spoken


def _month_day(match):
    month = MONTH_NUMBERS[match.group(1).lower()]
    spoken = date_without_year_to_words(int(match.group(2)), month)
    if spoken is None:
        return match.group(0)
    return spoken


def _iso(match):
    return _finish(match, int(match.group(3)), int(match.group(2)), int(match.group(1)))


def _slash(match):
    # DD/MM/YYYY: the FIRST number is the day.
    return _finish(match, int(match.group(1)), int(match.group(2)), int(match.group(3)))


def convert_dates(text):
    """Replace every date in text with words."""
    text = DAY_MONTH_YEAR.sub(_day_month_year, text)
    text = MONTH_DAY_YEAR.sub(_month_day_year, text)
    text = ISO_DATE.sub(_iso, text)
    text = SLASH_DATE.sub(_slash, text)
    # Year-less dates run last, so a date WITH a year is never read as one without.
    text = DAY_MONTH.sub(_day_month, text)
    text = MONTH_DAY.sub(_month_day, text)
    return text


def _bare_year(match):
    # Keep the word and the spacing exactly as written, only the number changes.
    return match.group(1) + match.group(2) + year_to_words(int(match.group(3)))


def convert_bare_years(text):
    """Read a year like 2025 after words such as "in" or "since" as a year."""
    return BARE_YEAR.sub(_bare_year, text)
