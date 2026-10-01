import logging

from ocr import extract_text
from granite import analyze_text
from scout_engine import calculate_scout_score

logger = logging.getLogger(__name__)


def analyze_listing(image_path: str):
    """Run an image through OCR, Granite analysis, and Scout scoring."""
    ocr_text = ""
    try:
        ocr_text = extract_text(image_path)
        analysis = analyze_text(ocr_text)

        if not analysis.get("success"):
            return {
                "success": False,
                "ocr_text": ocr_text,
                "listing": None,
                "scout": None,
                "error": analysis.get("error", "Granite analysis failed."),
            }

        listing = analysis["listing"]
        scout = calculate_scout_score(listing)
        return {
            "success": True,
            "ocr_text": ocr_text,
            "listing": listing,
            "scout": scout,
        }
    except Exception as exc:
        logger.exception("Failed to analyze listing: %s", exc)
        return {
            "success": False,
            "ocr_text": ocr_text,
            "listing": None,
            "scout": None,
            "error": str(exc),
        }