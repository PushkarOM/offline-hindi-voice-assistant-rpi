import re
import unicodedata
import math
from collections import Counter
from nlp.intents import INTENTS
from nlp.number_normalizer import normalize_numbers


FILLERS = [
    "जरा",
    "कृपया",
    "प्लीज",
    "please",
    "तो",
    "ज़रा"
]

# Hindi structural stopwords 
STOPWORDS = {
    "क्या", "है", "का", "की", "के",
    "कौन", "सा", "सी",
    "कितना", "कितनी", "कितने",
    "आज",   
}


def normalize(text):
    if not text:
        return ""

    text = text.lower().strip()
    text = unicodedata.normalize("NFKC", text)

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

    text = re.sub(r"\s+", " ", text)
    return text


def remove_fillers(text):
    for word in FILLERS:
        text = text.replace(word, "")
    return re.sub(r"\s+", " ", text).strip()



def clean_pattern(pattern):
    pattern = re.sub(r"\\s\*", " ", pattern)
    pattern = re.sub(r"\\s\+", " ", pattern)
    pattern = re.sub(r"\\b", "", pattern)
    pattern = re.sub(r"[()\[\]|?+^$]", " ", pattern)
    pattern = pattern.replace("\\", "")
    pattern = re.sub(r"\s+", " ", pattern)

    return pattern.strip()


def tokenize(text):
    return [
        word for word in text.split()
        if word not in STOPWORDS
    ]


def cosine_similarity(text1, text2):
    words1 = tokenize(text1)
    words2 = tokenize(text2)

    if not words1 or not words2:
        return 0.0

    vec1 = Counter(words1)
    vec2 = Counter(words2)

    intersection = set(vec1.keys()) & set(vec2.keys())
    dot_product = sum(vec1[w] * vec2[w] for w in intersection)

    magnitude1 = math.sqrt(sum(v * v for v in vec1.values()))
    magnitude2 = math.sqrt(sum(v * v for v in vec2.values()))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


def pattern_score(pattern, text):
    clean = clean_pattern(pattern)

    if not clean:
        return 0.0

    score = cosine_similarity(clean, text)

    # print(
    #     set(tokenize(clean)),
    #     set(tokenize(text)),
    #     score
    # )

    return score


def extract_timer_duration(text):
    """
    Extract timer duration using token parsing.
    Assumes numbers are already normalized to digits.
    Supports:
        - 10 मिनट
        - 5 सेकंड
        - 1 मिनट 30 सेकंड
        - 2 minute 10 second
    """

    tokens = text.split()
    total_seconds = 0

    # print(tokens)

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token.isdigit():
            value = int(token)

            # Look ahead safely
            if i + 1 < len(tokens):
                unit = tokens[i + 1]

                if unit in ("मिनट", "मिनिट"):
                    total_seconds += value * 60
                    i += 2
                    continue

                elif unit in ("सेकंड",'सेकेंड'):
                    total_seconds += value
                    i += 2
                    continue

        i += 1

    # print(total_seconds)
    return total_seconds if total_seconds > 0 else None


def detect_intent(text):
    if not text:
        return None

    text = normalize(text)
    text = remove_fillers(text)
    text = normalize_numbers(text)
    # print(text)

    # Exact Regex match
    for intent, patterns in INTENTS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return intent, text

    # if Regex Fails, Cosin Similarity is used
    best_intent = None
    best_score = 0.0

    for intent, patterns in INTENTS.items():
        for pattern in patterns:
            score = pattern_score(pattern, text)

            if score > best_score:
                best_score = score
                best_intent = intent

    if best_score >= 0.35:
        return best_intent , text

    return "UNKNOWN" , text
