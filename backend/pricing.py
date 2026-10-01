"""
pricing.py

Curated market value ranges used by Scout Engine.

Version 1 only supports a limited number of products.
"""

MARKET_VALUES = {

    "iphone": {
        "low": 500,
        "high": 1200
    },

    "macbook": {
        "low": 600,
        "high": 2000
    },

    "playstation": {
        "low": 250,
        "high": 700
    }

}


def get_market_range(product_name):

    if product_name is None:
        return None

    product = product_name.lower()

    if "iphone" in product:
        return MARKET_VALUES["iphone"]

    if "macbook" in product:
        return MARKET_VALUES["macbook"]

    if "playstation" in product or "ps5" in product or "ps4" in product:
        return MARKET_VALUES["playstation"]

    return None


def supported_product(product_name):

    if product_name is None:
        return False

    product = product_name.lower()

    supported = [

        "iphone",

        "macbook",

        "playstation",

        "ps5",

        "ps4"

    ]

    return any(x in product for x in supported)