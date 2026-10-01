import json
import logging
import ollama

from prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

MODEL = "granite3.2-vision:2b"


PRODUCT_ALIASES = {

    "ps5": "PlayStation 5",
    "playstation 5": "PlayStation 5",
    "playstation": "PlayStation 5",

    "ps4": "PlayStation 4",
    "playstation 4": "PlayStation 4",

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


def normalize_listing(listing):

    product = (listing.get("product_name") or "").lower()

    for alias, official in PRODUCT_ALIASES.items():

        if alias in product:

            listing["product_name"] = official

            break

    return listing


def analyze_text(text: str):

    if not text:

        return {

            "success": False,

            "error": "No OCR text."

        }

    prompt = f"""
The following text was extracted from a Facebook Marketplace screenshot.

Ignore browser text, URLs, dates, weather, page navigation,
and application names.

Extract ONLY the Marketplace listing.

Marketplace Listing:

{text}

Return ONLY valid JSON.
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

        listing = json.loads(

            response["message"]["content"]

        )

        listing = normalize_listing(listing)

        return {

            "success": True,

            "listing": listing

        }

    except Exception as e:

        logger.exception(e)

        return {

            "success": False,

            "error": str(e)

        }