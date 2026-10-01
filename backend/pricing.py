"""
pricing.py

Supported products and estimated market ranges.
"""

PRODUCTS = {

    # ------------------------
    # Apple
    # ------------------------

    "iphone": {
        "aliases": ["iphone"],
        "category": "Phone",
        "low": 350,
        "high": 1500
    },

    "ipad": {
        "aliases": ["ipad"],
        "category": "Tablet",
        "low": 200,
        "high": 1200
    },

    "macbook": {
        "aliases": ["macbook", "macbook pro", "macbook air"],
        "category": "Laptop",
        "low": 500,
        "high": 2500
    },

    "apple watch": {
        "aliases": ["apple watch"],
        "category": "Wearable",
        "low": 120,
        "high": 900
    },

    "airpods": {
        "aliases": ["airpods", "airpods pro", "airpods max"],
        "category": "Audio",
        "low": 60,
        "high": 650
    },

    # ------------------------
    # Samsung / Google
    # ------------------------

    "samsung galaxy": {
        "aliases": ["galaxy", "samsung"],
        "category": "Phone",
        "low": 200,
        "high": 1400
    },

    "google pixel": {
        "aliases": ["pixel", "google pixel"],
        "category": "Phone",
        "low": 200,
        "high": 1200
    },

    # ------------------------
    # Windows Laptops
    # ------------------------

    "surface": {
        "aliases": ["surface"],
        "category": "Laptop",
        "low": 300,
        "high": 1800
    },

    "dell": {
        "aliases": ["dell", "xps"],
        "category": "Laptop",
        "low": 250,
        "high": 1800
    },

    "hp": {
        "aliases": ["hp", "spectre"],
        "category": "Laptop",
        "low": 250,
        "high": 1800
    },

    "lenovo": {
        "aliases": ["lenovo", "thinkpad"],
        "category": "Laptop",
        "low": 250,
        "high": 1800
    },

    # ------------------------
    # Gaming
    # ------------------------

    "playstation": {
        "aliases": [
            "playstation",
            "ps5",
            "ps4",
            "playstation 5",
            "playstation 4"
        ],
        "category": "Gaming",
        "low": 200,
        "high": 700
    },

    "xbox": {
        "aliases": [
            "xbox",
            "series x",
            "series s",
            "xbox one"
        ],
        "category": "Gaming",
        "low": 180,
        "high": 700
    },

    "switch": {
        "aliases": [
            "switch",
            "nintendo switch"
        ],
        "category": "Gaming",
        "low": 150,
        "high": 500
    },

    "steam deck": {
        "aliases": [
            "steam deck"
        ],
        "category": "Gaming",
        "low": 250,
        "high": 700
    }

}


def normalize_product(product_name):

    if not product_name:
        return None

    product = product_name.lower()

    for key, value in PRODUCTS.items():

        for alias in value["aliases"]:

            if alias in product:

                return key

    return None


def supported_product(product_name):

    return normalize_product(product_name) is not None


def get_market_range(product_name):

    normalized = normalize_product(product_name)

    if normalized is None:
        return None

    return {

        "low": PRODUCTS[normalized]["low"],

        "high": PRODUCTS[normalized]["high"]

    }


def get_category(product_name):

    normalized = normalize_product(product_name)

    if normalized is None:
        return None

    return PRODUCTS[normalized]["category"]
