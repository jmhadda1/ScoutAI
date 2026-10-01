from pricing import get_market_range, supported_product


def calculate_scout_score(listing):

    product = listing.get("product_name")
    asking_price = listing.get("asking_price")
    description = (listing.get("description") or "").strip()
    condition = (listing.get("condition") or "").strip()
    storage = (listing.get("storage") or "").strip()
    seller_notes = (listing.get("seller_notes") or "").strip()

    # ----------------------------
    # Supported Product
    # ----------------------------

    if not supported_product(product):

        return {
            "score": 0,
            "rating": "Unsupported Product",
            "recommendation":
                "Scout AI does not currently support this product category.",
            "market_range": None,
            "reasons": [
                "Unsupported product category."
            ]
        }

    market = get_market_range(product)

    market_low = market["low"]
    market_high = market["high"]

    score = 50
    reasons = []

    # ----------------------------
    # Price
    # ----------------------------

    if asking_price is None:

        score -= 15

        reasons.append("Unable to identify asking price.")

    else:

        if asking_price < market_low * 0.60:

            score -= 30

            reasons.append(
                "Price is much lower than expected market value."
            )

        elif asking_price < market_low:

            score -= 10

            reasons.append(
                "Price is below typical market value."
            )

        elif asking_price <= market_high:

            score += 20

            reasons.append(
                "Listing price falls within the expected market range."
            )

        elif asking_price <= market_high * 1.20:

            score += 5

            reasons.append(
                "Price is slightly above market value."
            )

        else:

            score -= 15

            reasons.append(
                "Price is well above market value."
            )

    # ----------------------------
    # Description
    # ----------------------------

    if len(description) >= 60:

        score += 10

        reasons.append(
            "Listing contains a detailed description."
        )

    elif len(description) >= 25:

        score += 5

        reasons.append(
            "Listing contains a basic description."
        )

    else:

        score -= 10

        reasons.append(
            "Description is very limited."
        )

    # ----------------------------
    # Condition
    # ----------------------------

    if condition:

        score += 10

        reasons.append(
            "Item condition identified."
        )

    else:

        score -= 10

        reasons.append(
            "Condition not specified."
        )

    # ----------------------------
    # Storage
    # ----------------------------

    if storage:

        score += 5

        reasons.append(
            "Storage capacity identified."
        )

    else:

        score -= 5

        reasons.append(
            "Storage capacity not specified."
        )

    # ----------------------------
    # Seller Notes
    # ----------------------------

    if len(seller_notes) >= 20:

        score += 5

    elif seller_notes:

        score += 2

    else:

        score -= 5

        reasons.append(
            "Very little seller information provided."
        )

    # ----------------------------
    # Clamp
    # ----------------------------

    score = max(0, min(100, score))

    # ----------------------------
    # Rating
    # ----------------------------

    if score >= 90:

        rating = "Excellent Buy"

        recommendation = (
            "Everything looks strong. Verify the item in person before purchasing."
        )

    elif score >= 75:

        rating = "Good Buy"

        recommendation = (
            "Overall this appears to be a solid listing, but verify functionality before purchasing."
        )

    elif score >= 60:

        rating = "Fair Buy"

        recommendation = (
            "Some important information is missing. Ask the seller additional questions before meeting."
        )

    elif score >= 40:

        rating = "Caution"

        recommendation = (
            "Several risk factors were detected. Proceed carefully."
        )

    else:

        rating = "High Risk"

        recommendation = (
            "This listing contains multiple warning signs. Exercise caution before proceeding."
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