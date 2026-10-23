"""Expand short written forms into the words a voice should say.

To add an abbreviation, add one line to ABBREVIATIONS. Matching is case sensitive,
so "Dr." matches but "dr." does not.

Known simplifications:
  - "St." always becomes "Street" (it could also mean "Saint").
  - Units are always plural: "1 km" becomes "one kilometers".
"""

import re

ABBREVIATIONS = {
    "Dr.": "Doctor",
    "Mr.": "Mister",
    "Mrs.": "Missus",
    "Ms.": "Miss",
    "Prof.": "Professor",
    "St.": "Street",
    "vs.": "versus",
    "etc.": "et cetera",
    "e.g.": "for example",
    "i.e.": "that is",
    "km": "kilometers",
    "kg": "kilograms",
    "%": "percent",
}


def expand_abbreviations(text):
    """Replace each abbreviation in the dictionary with its spoken form."""
    for short, spoken in ABBREVIATIONS.items():
        # (?<![A-Za-z]) means: not in the middle of a word ("Mst." is not "St.").
        # (?![A-Za-z]) means: the abbreviation must end the word ("kmh" is not "km").
        pattern = r"(?<![A-Za-z])" + re.escape(short) + r"(?![A-Za-z])"
        text = re.sub(pattern, spoken, text)
    return text
