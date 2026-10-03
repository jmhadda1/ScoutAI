from pricing import (
    get_market_range,
    supported_product,
    get_category
)


def add_positive(reasons, text):
    reasons.append({
        "type": "positive",
        "text": text
    })


def add_warning(reasons, risks, text, risk_text=None):
    reasons.append({
        "type": "warning",
        "text": text
    })

    if risk_text:
        risks.append(risk_text)


def calculate_scout_score(listing):

    product = listing.get("product_name")
    asking_price = listing.get("asking_price")

    description = (
        listing.get("description") or ""
    ).strip()

    condition = (
        listing.get("condition") or ""
    ).strip()

    seller_notes = (
        listing.get("seller_notes") or ""
    ).strip()

    details = listing.get("details") or {}

    storage = details.get("storage")
    model_variant = details.get("model_variant")
    carrier = details.get("carrier")
    unlocked = details.get("unlocked")
    battery_health = details.get("battery_health")
    paid_off = details.get("paid_off")
    functionality = details.get("functionality")
    accessories = details.get("accessories") or []
    damage = details.get("damage")

    # ---------------------------------
    # Supported Product
    # ---------------------------------

    if not supported_product(product):

        return {
            "score": 0,
            "rating": "Unsupported Product",
            "recommendation":
                "Scout AI does not currently support this product category.",
            "market_range": None,
            "reasons": [
                {
                    "type": "warning",
                    "text": "Unsupported product category."
                }
            ]
        }

    market = get_market_range(product)
    category = get_category(product)

    market_low = market["low"]
    market_high = market["high"]

    # Listings earn confidence.
    score = 20

    reasons = []
    risks = []

    # ---------------------------------
    # Product Identification
    # ---------------------------------

    if product:

        score += 10

        add_positive(
            reasons,
            "Product successfully identified."
        )

    # ---------------------------------
    # Price
    # ---------------------------------

    if asking_price is None:

        add_warning(
            reasons,
            risks,
            "Asking price could not be identified.",
            "the asking price could not be verified"
        )

    elif asking_price < market_low * 0.60:

        score -= 20

        add_warning(
            reasons,
            risks,
            "Price is significantly below the expected market range.",
            "the asking price is significantly below the expected market range"
        )

    elif asking_price < market_low:

        score += 5

        add_warning(
            reasons,
            risks,
            "Price is below the typical market range.",
            "the asking price is below the typical market range"
        )

    elif asking_price <= market_high:

        score += 15

        add_positive(
            reasons,
            "Price falls within the expected market range."
        )

    elif asking_price <= market_high * 1.20:

        score += 5

        add_warning(
            reasons,
            risks,
            "Price is slightly above the expected market range.",
            "the asking price is slightly above the expected market range"
        )

    else:

        score -= 10

        add_warning(
            reasons,
            risks,
            "Price is well above the expected market range.",
            "the asking price is well above the expected market range"
        )

    # ---------------------------------
    # Condition
    # ---------------------------------

    if condition:

        score += 10

        add_positive(
            reasons,
            "Item condition is stated."
        )

    else:

        add_warning(
            reasons,
            risks,
            "Item condition is not specified.",
            "the item's condition is not specified"
        )

    # ---------------------------------
    # Description Quality
    # ---------------------------------

    combined_text = (
        f"{description} {seller_notes}"
    ).strip()

    if len(combined_text) >= 100:

        score += 15

        add_positive(
            reasons,
            "Listing provides detailed product information."
        )

    elif len(combined_text) >= 50:

        score += 10

        add_positive(
            reasons,
            "Listing provides useful product information."
        )

    elif len(combined_text) >= 25:

        score += 3

        add_warning(
            reasons,
            risks,
            "Listing provides limited product information.",
            "the listing provides limited product information"
        )

    else:

        add_warning(
            reasons,
            risks,
            "Listing provides very little product information.",
            "the listing provides very little product information"
        )

    # ---------------------------------
    # Explicit Damage
    # ---------------------------------

    if damage:

        score -= 20

        add_warning(
            reasons,
            risks,
            f"Seller discloses item damage ({damage}).",
            f"the seller discloses item damage ({damage.lower()})"
        )

    # =================================================
    # PHONE-SPECIFIC CHECKS
    # =================================================

    if category == "Phone":

        # ---------------------------------
        # Paid-Off Status
        # ---------------------------------

        if paid_off is True:

            score += 8

            add_positive(
                reasons,
                "Seller states that the phone is paid off."
            )

        elif paid_off is False:

            score -= 15

            add_warning(
                reasons,
                risks,
                "Seller indicates that money is still owed on the phone.",
                "the phone may still have an outstanding balance"
            )

        else:

            add_warning(
                reasons,
                risks,
                "Paid-off status is not specified.",
                "paid-off status should be verified"
            )

        # ---------------------------------
        # Carrier / Unlock Status
        # ---------------------------------

        if unlocked is True:

            score += 5

            add_positive(
                reasons,
                "Seller states that the phone is unlocked."
            )

        elif unlocked is False:

            add_warning(
                reasons,
                risks,
                "Phone is listed as carrier locked.",
                "the phone is carrier locked"
            )

            if carrier:

                add_positive(
                    reasons,
                    f"Carrier information is provided ({carrier})."
                )

        else:

            if carrier:

                score += 3

                add_positive(
                    reasons,
                    f"Carrier information is provided ({carrier})."
                )

            else:

                add_warning(
                    reasons,
                    risks,
                    "Carrier or unlocked status is not provided.",
                    "carrier or unlocked status is not provided"
                )

        # ---------------------------------
        # Battery Health
        # ---------------------------------

        if battery_health:

            score += 5

            add_positive(
                reasons,
                f"Battery information is provided ({battery_health})."
            )

        else:

            add_warning(
                reasons,
                risks,
                "Battery health is not provided.",
                "battery health is not provided"
            )

        # ---------------------------------
        # Storage
        # ---------------------------------

        if storage:

            score += 4

            add_positive(
                reasons,
                f"Storage capacity is identified ({storage})."
            )

        else:

            add_warning(
                reasons,
                risks,
                "Storage capacity is not specified."
            )

        # ---------------------------------
        # Functionality
        # ---------------------------------

        if functionality:

            score += 5

            add_positive(
                reasons,
                "Seller provides information about device functionality."
            )

        else:

            add_warning(
                reasons,
                risks,
                "Device functionality is not explicitly confirmed.",
                "device functionality is not explicitly confirmed"
            )

    # =================================================
    # GAMING-SPECIFIC CHECKS
    # =================================================

    elif category == "Gaming":

        # ---------------------------------
        # Console Configuration
        # ---------------------------------

        if model_variant:

            score += 5

            add_positive(
                reasons,
                f"Console configuration is identified ({model_variant})."
            )

        else:

            add_warning(
                reasons,
                risks,
                "Exact console configuration is not specified.",
                "the exact console configuration is not specified"
            )

        # ---------------------------------
        # Functionality
        # ---------------------------------

        if functionality:

            score += 10

            add_positive(
                reasons,
                "Seller explicitly describes the console's functionality."
            )

        else:

            add_warning(
                reasons,
                risks,
                "Console functionality is not explicitly confirmed.",
                "console functionality is not explicitly confirmed"
            )

        # ---------------------------------
        # Accessories
        # ---------------------------------

        if accessories:

            score += 5

            accessory_text = ", ".join(
                str(item) for item in accessories
            )

            add_positive(
                reasons,
                f"Included accessories are described ({accessory_text})."
            )

        else:

            add_warning(
                reasons,
                risks,
                "Included accessories are not clearly described.",
                "included accessories are not clearly described"
            )

        # ---------------------------------
        # Storage
        # Secondary for gaming consoles.
        # ---------------------------------

        if storage:

            score += 2

            add_positive(
                reasons,
                f"Storage capacity is identified ({storage})."
            )

    # =================================================
    # LAPTOP / TABLET CHECKS
    # =================================================

    elif category in ["Laptop", "Tablet"]:

        # ---------------------------------
        # Model Configuration
        # ---------------------------------

        if model_variant:

            score += 7

            add_positive(
                reasons,
                f"Model configuration is identified ({model_variant})."
            )

        else:

            add_warning(
                reasons,
                risks,
                "Exact model configuration is not specified.",
                "the exact model configuration is not specified"
            )

        # ---------------------------------
        # Storage
        # ---------------------------------

        if storage:

            score += 5

            add_positive(
                reasons,
                f"Storage capacity is identified ({storage})."
            )

        else:

            add_warning(
                reasons,
                risks,
                "Storage capacity is not specified.",
                "storage capacity is not specified"
            )

        # ---------------------------------
        # Functionality
        # ---------------------------------

        if functionality:

            score += 8

            add_positive(
                reasons,
                "Seller provides information about device functionality."
            )

        else:

            add_warning(
                reasons,
                risks,
                "Device functionality is not explicitly confirmed.",
                "device functionality is not explicitly confirmed"
            )

    # =================================================
    # OTHER CATEGORIES
    # =================================================

    else:

        if functionality:

            score += 5

            add_positive(
                reasons,
                "Seller provides information about item functionality."
            )

        if storage:

            score += 2

            add_positive(
                reasons,
                f"Storage capacity is identified ({storage})."
            )

    # ---------------------------------
    # Clamp Score
    # ---------------------------------

    score = max(
        0,
        min(100, score)
    )

    # ---------------------------------
    # Internal Rating
    # ---------------------------------

    if score >= 85:

        rating = "Excellent Buy"

    elif score >= 70:

        rating = "Good Buy"

    elif score >= 55:

        rating = "Fair Buy"

    elif score >= 40:

        rating = "Caution"

    else:

        rating = "High Risk"

    # ---------------------------------
    # Recommendation
    # ---------------------------------

    # Explicit physical damage should
    # always be prioritized.

    damage_risks = [
        risk for risk in risks
        if "damage" in risk.lower()
        or "cracked" in risk.lower()
        or "broken" in risk.lower()
    ]

    other_risks = [
        risk for risk in risks
        if risk not in damage_risks
    ]

    top_risks = (
        damage_risks + other_risks
    )[:3]

    if not top_risks:

        recommendation = (
            "No major concerns were detected from the available listing "
            "information. Verify the item in person before purchasing."
        )

    else:

        if len(top_risks) == 1:

            risk_text = top_risks[0]

        elif len(top_risks) == 2:

            risk_text = (
                f"{top_risks[0]} and "
                f"{top_risks[1]}"
            )

        else:

            risk_text = (
                f"{top_risks[0]}, "
                f"{top_risks[1]}, and "
                f"{top_risks[2]}"
            )

        if score >= 70:

            recommendation = (
                f"The listing has several positive signals, but note that "
                f"{risk_text}. Verify these details before purchasing."
            )

        elif score >= 40:

            recommendation = (
                f"Review carefully because {risk_text}. "
                f"Ask the seller to verify these details before meeting."
            )

        else:

            recommendation = (
                f"Proceed with caution because {risk_text}. "
                f"Do not rely on the listing alone; verify the item "
                f"and seller before proceeding."
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