from pricing import get_market_range, supported_product


def calculate_scout_score(listing):

    score = 100
    reasons = []

    product = listing.get("product_name")
    asking_price = listing.get("asking_price")
    description = listing.get("description") or ""
    condition = listing.get("condition")
    storage = listing.get("storage")

    # -----------------------------
    # Supported Product
    # -----------------------------

    if not supported_product(product):

        return {

            "score": 0,

            "rating": "Unsupported Product",

            "recommendation":
                "Scout AI Version 1 currently supports iPhones, MacBooks, and PlayStations.",

            "market_range": None,

            "reasons": [

                "Unsupported product category."

            ]

        }

    # -----------------------------
    # Market Value
    # -----------------------------

    market = get_market_range(product)

    market_low = market["low"]
    market_high = market["high"]

    if asking_price is None:

        score -= 20

        reasons.append("Unable to identify asking price.")

    else:

        if asking_price < market_low * 0.60:

            score -= 20

            reasons.append("Listing price is significantly below expected market value.")

        elif asking_price > market_high * 1.30:

            score -= 10

            reasons.append("Listing price is above expected market value.")

        else:

            reasons.append("Listing price falls within the expected market range.")

    # -----------------------------
    # Description
    # -----------------------------

    if len(description) < 20:

        score -= 10

        reasons.append("Listing description is limited.")

    else:

        reasons.append("Listing contains a detailed description.")

    # -----------------------------
    # Storage
    # -----------------------------

    if storage:

        reasons.append("Storage capacity identified.")

    else:

        score -= 5

        reasons.append("Storage capacity not specified.")

    # -----------------------------
    # Condition
    # -----------------------------

    if condition:

        reasons.append("Item condition identified.")

    else:

        score -= 5

        reasons.append("Item condition not specified.")

    # -----------------------------
    # Clamp Score
    # -----------------------------

    score = max(0, min(score, 100))

    # -----------------------------
    # Rating
    # -----------------------------

    if score >= 90:

        rating = "Excellent Buy"

        recommendation = (
            "This listing appears trustworthy based on the available information."
        )

    elif score >= 75:

        rating = "Good Buy"

        recommendation = (
            "Overall this listing looks reasonable, but review it carefully."
        )

    elif score >= 50:

        rating = "Fair Purchase"

        recommendation = (
            "Proceed carefully and verify the product before meeting."
        )

    else:

        rating = "High Risk"

        recommendation = (
            "Multiple warning signs were detected. Proceed with caution."
        )

    return {

        "score": score,

        "rating": rating,

        "recommendation": recommendation,

        "market_range": {

            "low": market_low,

            "high": market_high

        },

        "reasons": reasons

    }