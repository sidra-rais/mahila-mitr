"""
Matching Algorithm Module for Mahila Mitr System
Calculates suitability match scores between Help Requests and Mahila Mitr volunteers.
"""

from storage import load_json


def calculate_match_score(help_request, mitr):
    """
    Calculates a transparent, rule-based compatibility score (0-100)
    between a Help Request and a Mahila Mitr candidate.

    Scoring Breakdown:
    - Availability: 30 pts (Must be available to receive high score)
    - Area Proximity: 40 pts (Exact match), 15 pts (Cross-area fallback)
    - Assistance Type: 20 pts (Exact match), 10 pts (General assistance)
    - Urgency Compatibility Bonus: 10 pts (Active available responder during High urgency)
    """
    score = 0
    reasons = []

    # 1. Availability check (30 pts)
    if mitr.get("is_available", True):
        score += 30
        reasons.append("Currently available (+30)")
    else:
        reasons.append("Currently busy (0)")

    # 2. Area match (40 pts)
    req_area = help_request.get("area", "").strip().lower()
    mitr_area = mitr.get("area", "").strip().lower()
    if req_area and mitr_area and req_area == mitr_area:
        score += 40
        reasons.append(f"Located in same area: {mitr.get('area')} (+40)")
    else:
        score += 15
        reasons.append(f"Different area: {mitr.get('area')} (+15)")

    # 3. Assistance type compatibility (20 pts)
    req_asst = help_request.get("assistance_needed", "").strip().lower()
    mitr_asst = mitr.get("assistance_type", "").strip().lower()

    if req_asst and mitr_asst and req_asst == mitr_asst:
        score += 20
        reasons.append(f"Exact match for skill: '{mitr.get('assistance_type')}' (+20)")
    elif mitr_asst == "general assistance":
        score += 10
        reasons.append("Offers General assistance (+10)")
    else:
        score += 5
        reasons.append("Cross-functional assistance (+5)")

    # 4. Urgency compatibility (10 pts)
    urgency = help_request.get("urgency", "Medium").strip().lower()
    if urgency == "high" and mitr.get("is_available", True):
        score += 10
        reasons.append("High urgency priority compatibility (+10)")
    elif urgency == "medium":
        score += 5
        reasons.append("Standard response window (+5)")

    # Clamp score to 0-100
    final_score = max(0, min(100, score))
    return final_score, reasons


def find_suitable_mitrs(help_request, top_n=3):
    """
    Evaluates all registered Mahila Mitrs and ranks them by suitability score.
    Returns list of tuples: (mitr_dict, score, reason_list) sorted highest first.
    """
    all_mitrs = load_json("mahila_mitrs.json", default=[])
    if not all_mitrs:
        return []

    scored_candidates = []
    for mitr in all_mitrs:
        score, reasons = calculate_match_score(help_request, mitr)
        scored_candidates.append((mitr, score, reasons))

    # Sort descending by score, and secondarily by help_count (experience)
    scored_candidates.sort(key=lambda item: (item[1], item[0].get("help_count", 0)), reverse=True)

    return scored_candidates[:top_n]
