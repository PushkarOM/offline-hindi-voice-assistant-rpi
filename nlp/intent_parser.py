import re
import unicodedata
from nlp.intents import INTENTS
from rapidfuzz import fuzz


# Common filler / polite words to ignore
FILLERS = [
    "जरा",
    "कृपया",
    "प्लीज",
    "please",
    "तो",
    "ज़रा"
]

def fuzzy_pattern_match(pattern, text, threshold=82):
    """
    Try fuzzy matching when regex fails.
    Extract literal words from regex pattern and compare.
    """
    # Remove regex symbols to get approximate keyword
    clean_pattern = re.sub(r"[\\b\(\)\|\?\*\+\[\]\^$]", "", pattern)
    clean_pattern = clean_pattern.replace("\\s*", " ").strip()

    if not clean_pattern:
        return False

    score = fuzz.partial_ratio(clean_pattern, text)
    return score >= threshold


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

def extract_timer_duration(text):
    # Seconds
    match = re.search(r"(\d+)\s*(सेकंड|second)", text)
    if match:
        return int(match.group(1))

    # Minutes
    match = re.search(r"(\d+)\s*(मिनट|मिनिट|minute)", text)
    if match:
        return int(match.group(1)) * 60

    return None


def detect_intent(text):
    if not text:
        return None

    text = normalize(text)
    text = remove_fillers(text)

    # Exact regex match
    for intent, patterns in INTENTS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return intent


    # Fuzzy match (for ASR mistakes / regex doesn't work) 
    best_intent = None
    best_score = 0

    for intent, patterns in INTENTS.items():
        for pattern in patterns:
            clean_pattern = re.sub(r"[\\b\(\)\|\?\*\+\[\]\^$]", "", pattern)
            clean_pattern = clean_pattern.replace("\\s*", " ").strip()

            if not clean_pattern:
                continue

            score = fuzz.partial_ratio(clean_pattern, text)

            if score > best_score:
                best_score = score
                best_intent = intent

    if best_score >= 82:
        return best_intent

    return "UNKNOWN"
