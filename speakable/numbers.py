"""Turn numbers into spoken English words.

Two number systems are supported:
  - "international": thousand, million, billion  (1,000,000 = ten lakh in Indian)
  - "indian":        thousand, lakh, crore       (1,00,000 = one lakh)

Supported range: 0 up to 999,999,999,999 (just under one trillion).
Anything bigger raises a ValueError with a clear message.
"""

# Words for 0 to 19. The position in the list IS the number, so ONES[7] is "seven".
ONES = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
]

# Words for the tens. TENS[2] is "twenty". Positions 0 and 1 are unused.
TENS = [
    "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
    "eighty", "ninety",
]

# The biggest number we promise to read out loud.
MAX_SUPPORTED = 999999999999

# Each pair is (size of the unit, its name). We go from the biggest to the smallest.
INTERNATIONAL_SCALES = [
    (1000000000, "billion"),
    (1000000, "million"),
    (1000, "thousand"),
]
INDIAN_SCALES = [
    (10000000, "crore"),
    (100000, "lakh"),
    (1000, "thousand"),
]

# Ordinals that are not just "word + th". Example: "one" becomes "first".
ORDINAL_SPECIAL = {
    "one": "first",
    "two": "second",
    "three": "third",
    "five": "fifth",
    "eight": "eighth",
    "nine": "ninth",
    "twelve": "twelfth",
}


def _below_thousand(n):
    """Words for 0 to 999. Returns an empty string for 0 (used when joining parts)."""
    words = []
    hundreds = n // 100
    rest = n % 100

    if hundreds > 0:
        words.append(ONES[hundreds])
        words.append("hundred")

    if rest >= 20:
        words.append(TENS[rest // 10])
        if rest % 10 > 0:
            words.append(ONES[rest % 10])
    elif rest > 0:
        words.append(ONES[rest])

    return " ".join(words)


def _words_with_scales(n, scales):
    """Read n using a list of (size, name) scales, biggest first."""
    parts = []
    for size, name in scales:
        chunk = n // size
        if chunk > 0:
            # In the Indian system the crore chunk can be bigger than 999
            # (for example 5,000 crore), so we read the chunk the same way again.
            if chunk >= 1000:
                chunk_words = _words_with_scales(chunk, scales)
            else:
                chunk_words = _below_thousand(chunk)
            parts.append(chunk_words + " " + name)
            n = n % size
    if n > 0:
        parts.append(_below_thousand(n))
    return " ".join(parts)


def int_to_words(n, system="international"):
    """Convert a whole number to words. Example: 1250 -> "one thousand two hundred fifty"."""
    if system not in ("international", "indian"):
        raise ValueError("system must be 'international' or 'indian', got: " + str(system))

    if n < 0:
        return "minus " + int_to_words(-n, system)

    if n > MAX_SUPPORTED:
        raise ValueError(
            "number is too large, the supported range is 0 to "
            + "{:,}".format(MAX_SUPPORTED)
        )

    if n == 0:
        return "zero"

    if system == "indian":
        return _words_with_scales(n, INDIAN_SCALES)
    return _words_with_scales(n, INTERNATIONAL_SCALES)


def digits_to_words(digits):
    """Read digits one by one. Example: "14" -> "one four". Used after a decimal point."""
    words = []
    for ch in digits:
        words.append(ONES[int(ch)])
    return " ".join(words)


def number_to_words(text, system="international"):
    """Convert number text such as "1,250", "-0.5" or "3.14" to words.

    Commas are ignored. Digits after the point are read one by one.
    """
    cleaned = text.strip().replace(",", "")

    negative = cleaned.startswith("-")
    if negative:
        cleaned = cleaned[1:]

    fraction = None
    whole = cleaned
    if "." in cleaned:
        whole, fraction = cleaned.split(".", 1)
    if whole == "":
        whole = "0"

    if not whole.isdigit():
        raise ValueError("not a number: " + text)
    if fraction is not None and not fraction.isdigit():
        raise ValueError("not a number: " + text)

    words = int_to_words(int(whole), system)
    if fraction is not None:
        words = words + " point " + digits_to_words(fraction)
    if negative:
        words = "minus " + words
    return words


def ordinal_words(value):
    """Convert 22 or "22nd" to "twenty second". Only the LAST word becomes an ordinal."""
    text = str(value).strip().lower().replace(",", "")
    # Remove a suffix such as "st", "nd", "rd", "th" if there is one.
    text = text.rstrip("abcdefghijklmnopqrstuvwxyz")
    if not text.isdigit():
        raise ValueError("not an ordinal number: " + str(value))

    words = int_to_words(int(text)).split(" ")
    last = words[-1]

    if last in ORDINAL_SPECIAL:
        last = ORDINAL_SPECIAL[last]
    elif last.endswith("y"):
        # twenty -> twentieth
        last = last[:-1] + "ieth"
    else:
        # four -> fourth, hundred -> hundredth
        last = last + "th"

    words[-1] = last
    return " ".join(words)
