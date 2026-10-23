"""Turn money amounts such as "Rs. 1,250.50" or "$5" into spoken words.

Supported currencies (the symbol or code must come BEFORE the amount):
  INR: ₹, Rs., Rs, INR  -> rupees and paise
  USD: $, USD           -> dollars and cents

Convention: digits after the point are read as the minor unit (paise or cents).
"$1.5" means one dollar and fifty cents. More than two decimal digits are cut off.
"""

import re

from speakable.numbers import int_to_words

# Maps what the user wrote (in lower case) to a currency code.
SYMBOL_TO_CODE = {
    "₹": "INR",
    "rs.": "INR",
    "rs": "INR",
    "inr": "INR",
    "$": "USD",
    "usd": "USD",
}

# For each code: (major singular, major plural, minor singular, minor plural).
CURRENCY_WORDS = {
    "INR": ("rupee", "rupees", "paisa", "paise"),
    "USD": ("dollar", "dollars", "cent", "cents"),
}

# Reads as: a currency symbol, optional space, the whole part (with optional commas,
# both 1,250 and Indian 1,25,000 style), then an optional decimal part.
# (?<![A-Za-z]) stops "cars 5" from being read as "Rs 5".
MONEY_PATTERN = re.compile(
    r"(?<![A-Za-z])(₹|Rs\.?|INR|\$|USD)\s?(\d{1,3}(?:,\d{2,3})+|\d+)(\.\d+)?",
    re.IGNORECASE,
)


def _unit_name(count, singular, plural):
    """Pick "dollar" for exactly one, otherwise "dollars"."""
    if count == 1:
        return singular
    return plural


def money_to_words(code, whole_text, fraction_text, system="international"):
    """Build the spoken form. fraction_text looks like ".50" or is None."""
    major_one, major_many, minor_one, minor_many = CURRENCY_WORDS[code]

    whole = int(whole_text.replace(",", ""))

    minor = 0
    if fraction_text:
        # Keep two digits: ".5" becomes "50", ".505" becomes "50".
        two_digits = (fraction_text[1:] + "00")[:2]
        minor = int(two_digits)

    parts = []
    # Skip "zero dollars" when there are only cents, like "$0.50".
    if whole > 0 or minor == 0:
        parts.append(int_to_words(whole, system) + " " + _unit_name(whole, major_one, major_many))
    if minor > 0:
        parts.append(int_to_words(minor, system) + " " + _unit_name(minor, minor_one, minor_many))

    return " and ".join(parts)


def _replace_money(match, system):
    code = SYMBOL_TO_CODE[match.group(1).lower()]
    try:
        return money_to_words(code, match.group(2), match.group(3), system)
    except ValueError:
        # Number too large to read: leave the original text alone.
        return match.group(0)


def convert_money(text, system="international"):
    """Replace every money amount in text with words."""

    def replacer(match):
        return _replace_money(match, system)

    return MONEY_PATTERN.sub(replacer, text)
