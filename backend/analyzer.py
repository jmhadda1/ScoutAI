import logging
import re

from ocr import extract_text
from granite import analyze_text
from scout_engine import calculate_scout_score

logger = logging.getLogger(__name__)


# ============================================================
# PRICE
# ============================================================

def extract_price(text: str):

    if not text:
        return None

    patterns = [
        r"\$\s?(\d{2,5})",
        r"\bS(\d{2,5})\b",
        r"\b(\d{2,5})\s?USD\b",
        r"\bUSD\s?(\d{2,5})",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            try:
                return int(match.group(1))

            except (ValueError, TypeError):
                continue

    return None


# ============================================================
# STORAGE
# ============================================================

def find_storage(text: str):

    if not text:
        return None

    match = re.search(
        r"\b(\d{2,4})\s?(GB|TB)\b",
        text,
        re.IGNORECASE
    )

    if not match:
        return None

    return (
        f"{match.group(1)}"
        f"{match.group(2).upper()}"
    )


# ============================================================
# DAMAGE
# ============================================================

def find_damage(text: str):

    if not text:
        return None

    damage_patterns = [
        (
            r"\bscreen\s+(?:is\s+)?cracked\b",
            "Cracked screen"
        ),
        (
            r"\bcracked\s+screen\b",
            "Cracked screen"
        ),
        (
            r"\bscreen\s+(?:is\s+)?broken\b",
            "Broken screen"
        ),
        (
            r"\bbroken\s+screen\b",
            "Broken screen"
        ),
        (
            r"\bwater\s+damage(?:d)?\b",
            "Water damage"
        ),
        (
            r"\bfor\s+parts\b",
            "Listed for parts"
        ),
        (
            r"\bdoes(?:n't| not)\s+work\b",
            "Item does not work"
        ),
        (
            r"\bnot\s+working\b",
            "Item does not work"
        ),
        (
            r"\b(?:is\s+)?damaged\b",
            "Physical damage disclosed"
        ),
        (
            r"\bbroken\b",
            "Damage disclosed"
        ),
        (
            r"\bcracked\b",
            "Crack/damage disclosed"
        )
    ]

    for pattern, label in damage_patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):
            return label

    return None


# ============================================================
# BATTERY HEALTH / BATTERY LIFE
# ============================================================

def find_battery_health(text: str):

    if not text:
        return None

    # ---------------------------------
    # Pattern 1:
    # battery health 89%
    # battery life 89%
    # battery 89%
    # ---------------------------------

    pattern_after = re.search(
        r"\bbattery"
        r"(?:\s+(?:health|life|capacity))?"
        r"[^0-9%]{0,20}"
        r"(\d{1,3})\s?%",
        text,
        re.IGNORECASE
    )

    if pattern_after:

        try:

            percent = int(
                pattern_after.group(1)
            )

            if 1 <= percent <= 100:
                return f"{percent}%"

        except (ValueError, TypeError):
            pass

    # ---------------------------------
    # Pattern 2:
    # 89% battery health
    # 89% battery life
    # 89% battery
    # ---------------------------------

    pattern_before = re.search(
        r"\b(\d{1,3})\s?%"
        r"[^a-zA-Z0-9]{0,10}"
        r"battery"
        r"(?:\s+(?:health|life|capacity))?",
        text,
        re.IGNORECASE
    )

    if pattern_before:

        try:

            percent = int(
                pattern_before.group(1)
            )

            if 1 <= percent <= 100:
                return f"{percent}%"

        except (ValueError, TypeError):
            pass

    return None


# ============================================================
# CARRIER
# ============================================================

def find_carrier(text: str):

    if not text:
        return None

    # Important:
    # use explicit word boundaries.
    #
    # Do NOT search for plain "att"
    # because OCR/browser text may contain
    # those letters inside unrelated words.

    carrier_patterns = [
        (
            r"\bverizon\b",
            "Verizon"
        ),
        (
            r"\bat\s*&\s*t\b",
            "AT&T"
        ),
        (
            r"\bat&t\b",
            "AT&T"
        ),
        (
            r"\bt[\s-]?mobile\b",
            "T-Mobile"
        ),
        (
            r"\bsprint\b",
            "Sprint"
        )
    ]

    for pattern, carrier in carrier_patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):
            return carrier

    return None


# ============================================================
# FUNCTIONALITY
# ============================================================

def find_functionality(text: str):

    if not text:
        return None

    functionality_patterns = [
        r"\bworks perfectly\b",
        r"\bworks great\b",
        r"\bworks fine\b",
        r"\bfully functional\b",
        r"\bfully functioning\b",
        r"\beverything works\b",
        r"\bworks as it should\b",
        r"\bno problems\b",
        r"\bno issues\b"
    ]

    for pattern in functionality_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(0)

    return None


# ============================================================
# MODEL VARIANT
# ============================================================

def find_model_variant(text: str):

    if not text:
        return None

    variant_patterns = [
        (
            r"\bps5\s+slim\b",
            "PS5 Slim"
        ),
        (
            r"\bps5\s+digital\b",
            "PS5 Digital"
        ),
        (
            r"\bdigital\s+edition\b",
            "Digital Edition"
        ),
        (
            r"\bdisc\s+edition\b",
            "Disc Edition"
        ),
        (
            r"\bmacbook\s+air\s+m[1-9]\b",
            None
        ),
        (
            r"\bmacbook\s+pro\s+m[1-9]\b",
            None
        )
    ]

    for pattern, label in variant_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            if label:
                return label

            return match.group(0)

    return None


# ============================================================
# VALIDATION
# ============================================================

def validate_details(listing, ocr_text):

    text = ocr_text.lower()

    details = listing.get("details")

    if not isinstance(details, dict):
        details = {}

    # ---------------------------------
    # Storage
    # ---------------------------------

    details["storage"] = find_storage(
        ocr_text
    )

    # ---------------------------------
    # Damage
    # ---------------------------------

    details["damage"] = find_damage(
        ocr_text
    )

    # ---------------------------------
    # Paid Off
    # ---------------------------------

    if re.search(
        r"\bpaid[\s-]?off\b",
        text,
        re.IGNORECASE
    ):

        details["paid_off"] = True

    elif re.search(
        r"\b(still owe|balance owed|not paid off)\b",
        text,
        re.IGNORECASE
    ):

        details["paid_off"] = False

    else:

        details["paid_off"] = None

    # ---------------------------------
    # Carrier
    # ---------------------------------

    details["carrier"] = find_carrier(
        ocr_text
    )

    # ---------------------------------
    # Unlocked Status
    # ---------------------------------

    if re.search(
        r"\b(factory\s+)?unlocked\b",
        text,
        re.IGNORECASE
    ):

        details["unlocked"] = True

    elif re.search(
        r"\b(carrier\s+locked|locked\s+to)\b",
        text,
        re.IGNORECASE
    ):

        details["unlocked"] = False

    else:

        details["unlocked"] = None

    # ---------------------------------
    # Battery
    # ---------------------------------

    details["battery_health"] = (
        find_battery_health(
            ocr_text
        )
    )

    # ---------------------------------
    # Functionality
    # ---------------------------------

    details["functionality"] = (
        find_functionality(
            ocr_text
        )
    )

    # ---------------------------------
    # Accessories
    #
    # V1 does not infer accessories
    # from photos.
    # ---------------------------------

    details["accessories"] = []

    # ---------------------------------
    # Model Variant
    # ---------------------------------

    details["model_variant"] = (
        find_model_variant(
            ocr_text
        )
    )

    listing["details"] = details

    return listing


# ============================================================
# MAIN ANALYSIS PIPELINE
# ============================================================

def analyze_listing(image_path: str):

    ocr_text = ""

    try:

        # ---------------------------------
        # OCR
        # ---------------------------------

        ocr_text = extract_text(
            image_path
        )

        # ---------------------------------
        # Deterministic Price Extraction
        # ---------------------------------

        detected_price = extract_price(
            ocr_text
        )

        # ---------------------------------
        # Granite AI Extraction
        # ---------------------------------

        analysis = analyze_text(
            ocr_text
        )

        if not analysis.get("success"):

            return {
                "success": False,
                "ocr_text": ocr_text,
                "listing": None,
                "scout": None,
                "error": analysis.get(
                    "error",
                    "Granite analysis failed."
                )
            }

        listing = analysis["listing"]

        # ---------------------------------
        # Verified Price Override
        # ---------------------------------

        if detected_price is not None:

            listing["asking_price"] = (
                detected_price
            )

        # ---------------------------------
        # Deterministic Validation Layer
        # ---------------------------------

        listing = validate_details(
            listing,
            ocr_text
        )

        # ---------------------------------
        # Scout Scoring Engine
        # ---------------------------------

        scout = calculate_scout_score(
            listing
        )

        return {
            "success": True,
            "ocr_text": ocr_text,
            "listing": listing,
            "scout": scout
        }

    except Exception as exc:

        logger.exception(
            "Listing analysis failed: %s",
            exc
        )

        return {
            "success": False,
            "ocr_text": ocr_text,
            "listing": None,
            "scout": None,
            "error": str(exc)
        }