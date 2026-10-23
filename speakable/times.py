"""Turn clock times into spoken words.

Conventions:
  9:30 am   -> nine thirty a m
  9 pm      -> nine p m              (minutes are optional with am/pm)
  12:00 pm  -> twelve o'clock p m    (on the hour we say o'clock)
  9:05 am   -> nine oh five a m      (minutes 1 to 9 get an "oh")
  21:05     -> twenty one oh five    (24 hour clock, no am/pm word)
  21:00     -> twenty one o'clock
  00:30     -> zero thirty
Invalid times (like 25:00) are left unchanged.
An am/pm that does not fit a 12 hour clock is dropped and the time is read the 24 hour way:
  13:00 pm  -> thirteen o'clock
  15:30 pm  -> fifteen thirty
  13 pm     -> thirteen
If even the 24 hour reading is impossible ("25:00 pm"), the text is left unchanged.
A trailing dot in "a.m." is swallowed as part of the time.
"""

import re

from speakable.numbers import int_to_words

# "9:30 am", "9 pm", "9:30 a.m."  (hour, optional minutes, then a or p)
TWELVE_HOUR = re.compile(
    r"(?<![\d:])(\d{1,2})(?::(\d{2}))?\s?([ap])(?:\.m\.|m\b)",
    re.IGNORECASE,
)
# "21:05" (hour, colon, two digit minutes). Not part of a longer number like 1:2:3.
TWENTY_FOUR_HOUR = re.compile(r"(?<![\d:.])(\d{1,2}):(\d{2})(?![\d:])")


def _minutes_to_words(minutes):
    """0 -> o'clock, 5 -> oh five, 30 -> thirty."""
    if minutes == 0:
        return "o'clock"
    if minutes < 10:
        return "oh " + int_to_words(minutes)
    return int_to_words(minutes)


def _twelve_hour(match):
    hour = int(match.group(1))
    minutes = 0
    if match.group(2) is not None:
        minutes = int(match.group(2))

    if hour < 1 or hour > 12 or minutes > 59:
        # Not a real 12 hour time. Drop the am/pm and use the 24 hour reading.
        if hour > 23 or minutes > 59:
            return match.group(0)
        spoken = int_to_words(hour)
        if match.group(2) is not None:
            spoken = spoken + " " + _minutes_to_words(minutes)
        return spoken

    spoken = int_to_words(hour)
    # With only "9 pm" there are no minutes to say.
    if match.group(2) is not None:
        spoken = spoken + " " + _minutes_to_words(minutes)

    # "a" becomes "a m", "p" becomes "p m", so a voice spells the letters out.
    return spoken + " " + match.group(3).lower() + " m"


def _twenty_four_hour(match):
    hour = int(match.group(1))
    minutes = int(match.group(2))

    if hour > 23 or minutes > 59:
        return match.group(0)

    return int_to_words(hour) + " " + _minutes_to_words(minutes)


def convert_times(text):
    """Replace every time in text with words."""
    # The am/pm form must run first, otherwise "9:30 am" would lose its "am".
    text = TWELVE_HOUR.sub(_twelve_hour, text)
    text = TWENTY_FOUR_HOUR.sub(_twenty_four_hour, text)
    return text
