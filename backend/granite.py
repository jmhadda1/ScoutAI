import json
import logging
import ollama

from prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

MODEL = "granite3.2-vision:2b"


def analyze_text(text: str):

    if not text:

        return {

            "success": False,

            "error": "No OCR text."

        }

    prompt = f"""
The following text was extracted from a Facebook Marketplace screenshot.

Ignore:

- browser interface
- tabs
- URLs
- dates
- times
- navigation text
- application names

Only extract information that belongs to the Marketplace listing itself.

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