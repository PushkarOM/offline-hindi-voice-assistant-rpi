import re
import unicodedata
from nlp.intents import INTENTS


# Common filler / polite words to ignore
FILLERS = [
    "जरा",
    "कृपया",
    "प्लीज",
    "please",
    "तो",
    "ज़रा"
]


def normalize(text):
    if not text:
        return ""

    # Lowercase + strip
    text = text.lower().strip()

    # Unicode normalization (handles hidden variations)
    text = unicodedata.normalize("NFKC", text)

    # Remove nukta variations
    replacements = {
        "ज़": "ज",
        "फ़": "फ",
        "ख़": "ख",
        "ग़": "ग",
        "क़": "क",
        "ड़": "ड",
        "ढ़": "ढ",
        "आवाज़": "आवाज"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text


def remove_fillers(text):
    for word in FILLERS:
        text = text.replace(word, "")
    return re.sub(r"\s+", " ", text).strip()


def detect_intent(text):
    if not text:
        return None

    text = normalize(text)
    text = remove_fillers(text)

    for intent, patterns in INTENTS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return intent

    return "UNKNOWN"
