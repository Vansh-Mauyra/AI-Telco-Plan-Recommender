def categorize_plans(plans, addons):
    categories = {
        "popular": [],
        "max saver": [],
        "unlimited 5g": [],
        "data heavy": [],
        "voice unlimited": [],
        "international roaming": [],
        "annual": [],
        "topup": []
    }

    for plan in plans:
        fee = plan["monthly_fee"]
        data = plan.get("data_gb") or 0
        daily = plan.get("daily_data_gb") or 0
        voice = plan.get("voice_minutes") or 0

        # Popular (balanced plans)
        if 399 <= fee <= 799 and daily >= 2:
            categories["popular"].append(plan)

        # Max Saver
        if fee <= 299:
            categories["max saver"].append(plan)

        # Unlimited 5G
        if plan["network_type"] in ("5G", "Both") and (data >= 150 or daily >= 2):
            categories["unlimited 5g"].append(plan)

        # Data Heavy
        if data >= 45 or daily >= 4:
            categories["data heavy"].append(plan)

        # Voice Unlimited
        if voice >= 3000:
            categories["voice unlimited"].append(plan)

        # International Roaming
        if plan["international_roaming"]:
            categories["international roaming"].append(plan)

        # Annual / Long validity
        if plan["validity_days"] >= 365:
            categories["annual"].append(plan)

    # Topups
    for addon in addons:
        categories["topup"].append(addon)

    return categories
