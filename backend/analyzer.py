import logging
import re

from ocr import extract_text
from granite import analyze_text
from scout_engine import calculate_scout_score

logger = logging.getLogger(__name__)


def extract_price(text: str):

    if not text:
        return None

    patterns = [

        r"\$\s?(\d{2,5})",      # $350
        r"\bS(\d{2,5})\b",      # OCR mistake: S350
        r"\b(\d{2,5})\s?USD\b", # 350 USD
        r"\bUSD\s?(\d{2,5})",
    ]

    for pattern in patterns:

        match = re.search(pattern, text, re.IGNORECASE)

        if match:

            try:

                return int(match.group(1))

            except:

                pass

    return None


def analyze_listing(image_path: str):

    ocr_text = ""

    try:

        ocr_text = extract_text(image_path)

        detected_price = extract_price(ocr_text)

        analysis = analyze_text(ocr_text)

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

        # ---------- PRICE OVERRIDE ----------

        if detected_price:

            listing["asking_price"] = detected_price

        # ------------------------------------

        scout = calculate_scout_score(listing)

        return {

            "success": True,

            "ocr_text": ocr_text,

            "listing": listing,

            "scout": scout

        }

    except Exception as exc:

        logger.exception(exc)

        return {

            "success": False,

            "ocr_text": ocr_text,

            "listing": None,

            "scout": None,

            "error": str(exc)

        }