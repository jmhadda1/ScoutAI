import json
import sys

from granite import analyze_text


OCR_TEXT = """
PS5

$350

Condition Used Good

Like new almost never use it

Phoenix
"""


def main():
    result = analyze_text(OCR_TEXT)
    print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
