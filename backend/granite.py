import json
import logging
import ollama

from prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

MODEL = "granite3.2-vision:2b"


PRODUCT_ALIASES = {
    "playstation 5": "PlayStation 5",
    "ps5": "PlayStation 5",

    "playstation 4": "PlayStation 4",
    "ps4": "PlayStation 4",

    "iphone": "iPhone",
    "ipad": "iPad",
    "macbook": "MacBook",

    "airpods": "AirPods",
    "apple watch": "Apple Watch",

    "galaxy": "Samsung Galaxy",
    "samsung": "Samsung Galaxy",

    "pixel": "Google Pixel",

    "surface": "Microsoft Surface",

    "xbox": "Xbox Series",

    "switch": "Nintendo Switch",

    "steam deck": "Steam Deck"
}


DETAIL_FIELDS = {
    "storage": None,
    "model_variant": None,
    "carrier": None,
    "unlocked": None,
    "battery_health": None,
    "paid_off": None,
    "functionality": None,
    "accessories": []
}


def normalize_product_name(product_name):

    if not product_name:
        return ""

    product_lower = product_name.lower()

    for alias, official in PRODUCT_ALIASES.items():

        if alias in product_lower:

            # Preserve useful model information when possible.
            if official == "iPhone":

                words = product_name.split()

                if len(words) > 1:
                    return product_name

            if official == "MacBook":

                words = product_name.split()

                if len(words) > 1:
                    return product_name

            return official

    return product_name


def normalize_listing(listing):

    if not isinstance(listing, dict):
        listing = {}

    listing["product_name"] = normalize_product_name(
        listing.get("product_name")
    )

    # ---------------------------------
    # Ensure required top-level fields
    # ---------------------------------

    defaults = {
        "brand": "",
        "category": "",
        "asking_price": None,
        "condition": "",
        "seller_notes": "",
        "description": "",
        "observations": []
    }

    for key, default in defaults.items():

        if key not in listing or listing[key] is None:

            if isinstance(default, list):
                listing[key] = []
            else:
                listing[key] = default

    # ---------------------------------
    # Normalize details object
    # ---------------------------------

    details = listing.get("details")

    if not isinstance(details, dict):
        details = {}

    normalized_details = {}

    for key, default in DETAIL_FIELDS.items():

        value = details.get(key)

        if key == "accessories":

            if isinstance(value, list):
                normalized_details[key] = value
            else:
                normalized_details[key] = []

        else:

            normalized_details[key] = (
                value if value not in ["", "unknown", "Unknown"] else None
            )

    listing["details"] = normalized_details

    # ---------------------------------
    # Clean observations
    # ---------------------------------

    if not isinstance(listing.get("observations"), list):
        listing["observations"] = []

    return listing


def analyze_text(text: str):

    if not text or not text.strip():

        return {
            "success": False,
            "error": "No OCR text."
        }

    prompt = f"""
The following text was extracted from a Facebook Marketplace screenshot.

Ignore browser text, URLs, dates, weather, navigation,
application names, buttons, and other interface text.

Extract ONLY factual information that belongs to the Marketplace listing.

Do not guess missing information.

Marketplace Listing:

{text}

Return ONLY valid JSON using the schema provided in the system prompt.
"""

    try:

        response = ollama.chat(
            model=MODEL,
            format="json",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        raw = response["message"]["content"]

        listing = json.loads(raw)

        listing = normalize_listing(listing)

        return {
            "success": True,
            "listing": listing
        }

    except json.JSONDecodeError:

        logger.exception(
            "Granite returned invalid JSON."
        )

        return {
            "success": False,
            "error": "Granite returned invalid JSON."
        }

    except Exception as e:

        logger.exception(
            "Granite analysis failed: %s",
            e
        )

        return {
            "success": False,
            "error": str(e)
        }