from rapidfuzz import process, fuzz
import re


# Base number map (0–99)
HINDI_NUMBERS = {
    # 0–20
    "शून्य": 0,
    "एक": 1,
    "दो": 2,
    "तीन": 3,
    "चार": 4,
    "पांच": 5,
    "छह": 6,
    "सात": 7,
    "आठ": 8,
    "नौ": 9,
    "दस": 10,
    "ग्यारह": 11,
    "बारह": 12,
    "तेरह": 13,
    "चौदह": 14,
    "पंद्रह": 15,
    "सोलह": 16,
    "सत्रह": 17,
    "अठारह": 18,
    "उन्नीस": 19,
    "बीस": 20,

    # 21–29
    "इक्कीस": 21,
    "बाईस": 22,
    "तेइस": 23,
    "चौबीस": 24,
    "पच्चीस": 25,
    "छब्बीस": 26,
    "सत्ताईस": 27,
    "अट्ठाईस": 28,
    "उनतीस": 29,

    # 30–39
    "तीस": 30,
    "इकतीस": 31,
    "बत्तीस": 32,
    "तैंतीस": 33,
    "चौंतीस": 34,
    "पैंतीस": 35,
    "छत्तीस": 36,
    "सैंतीस": 37,
    "अड़तीस": 38,
    "उनतालीस": 39,

    # 40–49
    "चालीस": 40,
    "इकतालीस": 41,
    "बयालीस": 42,
    "तैंतालीस": 43,
    "चवालीस": 44,
    "पैंतालीस": 45,
    "छियालीस": 46,
    "सैंतालीस": 47,
    "अड़तालीस": 48,
    "उनचास": 49,

    # 50–59
    "पचास": 50,
    "इक्यावन": 51,
    "बावन": 52,
    "तिरेपन": 53,
    "चौवन": 54,
    "पचपन": 55,
    "छप्पन": 56,
    "सत्तावन": 57,
    "अट्ठावन": 58,
    "उनसठ": 59,

    # 60
    "साठ": 60
}

# -------------------------------
# Normalize Hindi numbers in text

def normalize_numbers(text: str) -> str:

    words = text.split()
    converted = []

    for word in words:
        clean_word = re.sub(r"[^\w]", "", word)

        # Find best fuzzy match
        match = process.extractOne(
            clean_word,
            HINDI_NUMBERS.keys(),
            scorer=fuzz.ratio
        )

        if match and match[1] > 80:  # similarity threshold
            converted.append(str(HINDI_NUMBERS[match[0]]))
        else:
            converted.append(word)

    return " ".join(converted)
