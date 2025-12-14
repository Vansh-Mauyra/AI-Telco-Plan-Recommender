# app/services/scoring.py

def score_plan(plan: dict, user: dict, usage: dict) -> float:
    score = 0.0

    # Budget efficiency
    if plan["monthly_fee"] <= user["budget"]:
        score += 20

    # Data match
    data_diff = plan["data_gb"] - (usage.get("avg_data_gb") or 0)
    if data_diff >= 0:
        score += min(data_diff, 50)

    # Voice match
    voice_diff = plan["voice_minutes"] - (usage.get("avg_voice_minutes") or 0)
    if voice_diff >= 0:
        score += min(voice_diff / 100, 20)

    # Roaming needs
    if usage.get("uses_roaming") and plan["roaming_included"]:
        score += 15

    if usage.get("uses_international") and plan["international_roaming"]:
        score += 20

    # Network preference
    if plan["network_type"] == "5G":
        score += 10

    return score
