from threading import Lock
import re
import easyocr

_reader = None
_reader_lock = Lock()

IGNORE_PATTERNS = [

    "Evaluate Venture Idea",
    "Scout AI",
    "Swagger",
    "Search",
    "School",
    "Install",
    "ChatGPT",
    "Mostly clear",
    "Location is approximate",
    "facebook.com",
    "Marketplace",
    "Share",
    "Save",
    "Message",
    "Details",
    "Video Game Consoles",
    "Electronics",
]


def get_reader():

    global _reader

    if _reader is None:

        with _reader_lock:

            if _reader is None:

                _reader = easyocr.Reader(

                    ["en"],

                    gpu=False

                )

    return _reader


def clean_text(text: str):

    for pattern in IGNORE_PATTERNS:

        text = text.replace(pattern, "")

    text = re.sub(r"\b\d{1,2}:\d{2}\s?(AM|PM)\b", "", text)

    text = re.sub(r"\b\d+\u00b0F\b", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_text(image_path: str):

    reader = get_reader()

    results = reader.readtext(

        image_path,

        detail=0

    )

    text = " ".join(results)

    text = clean_text(text)

    print("\n========== OCR ==========\n")
    print(text)
    print("\n=========================\n")

    return text