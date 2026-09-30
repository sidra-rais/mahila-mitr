"""
Module 4 — Rule-Based Safety Risk Analyzer
Calculates transparent academic risk scores for areas based on severity, frequency, and community confirmations.
NOTE: This is an academic rule-based heuristic model for demo purposes.
"""

from storage import load_json
from utils import print_section

REPORTS_FILE = "safety_reports.json"


def calculate_area_risk(area_name):
    """
    Calculates a rule-based safety risk score (0-100) for a given area.

    Formula Breakdown:
    1. Severity Contribution (Max 50 pts):
       - High Severity:   20 pts each
       - Medium Severity: 10 pts each
       - Low Severity:    4 pts each
    2. Frequency Contribution (Max 30 pts):
       - Total Reports * 6 pts
    3. Community Confirmation Contribution (Max 20 pts):
       - Total Confirmations * 3 pts

    Risk Classification:
       0 - 30  : LOW
       31 - 60 : MEDIUM
       61 - 100: HIGH
    """
    reports = load_json(REPORTS_FILE, default=[])
    area_reports = [r for r in reports if r.get("area", "").strip().lower() == area_name.strip().lower()]

    if not area_reports:
        return {
            "area": area_name,
            "total_reports": 0,
            "category_counts": {},
            "severity_counts": {"High": 0, "Medium": 0, "Low": 0},
            "highest_severity": "None",
            "total_confirmations": 0,
            "risk_score": 0,
            "risk_level": "LOW",
            "primary_concern": "No reported concerns",
            "analysis": "No community safety concerns have been reported for this location.",
            "breakdown": {"severity_pts": 0, "frequency_pts": 0, "confirmation_pts": 0}
        }

    # Count categories and severities
    cat_counts = {}
    sev_counts = {"High": 0, "Medium": 0, "Low": 0}
    total_confirmations = 0

    for r in area_reports:
        cat = r.get("category", "Other")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

        sev = r.get("severity", "Medium")
        if sev in sev_counts:
            sev_counts[sev] += 1

        total_confirmations += int(r.get("confirmations", 1))

    # 1. Severity Points (Max 50)
    raw_sev_pts = (sev_counts["High"] * 20) + (sev_counts["Medium"] * 10) + (sev_counts["Low"] * 4)
    severity_pts = min(50, raw_sev_pts)

    # 2. Frequency Points (Max 30)
    frequency_pts = min(30, len(area_reports) * 6)

    # 3. Confirmation Points (Max 20)
    confirmation_pts = min(20, total_confirmations * 3)

    # Total Score clamped to 0-100
    risk_score = min(100, severity_pts + frequency_pts + confirmation_pts)

    # Classify Risk Level
    if risk_score >= 61:
        risk_level = "HIGH"
    elif risk_score >= 31:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # Highest severity observed
    if sev_counts["High"] > 0:
        highest_sev = "High"
    elif sev_counts["Medium"] > 0:
        highest_sev = "Medium"
    else:
        highest_sev = "Low"

    # Determine primary concern
    primary_concern = max(cat_counts.items(), key=lambda x: x[1])[0]

    # Generate summary analysis sentence
    if risk_level == "HIGH":
        analysis = (
            f"The area exhibits multiple critical concerns with significant community verification. "
            f"Caution is strongly advised, especially regarding '{primary_concern}'."
        )
    elif risk_level == "MEDIUM":
        analysis = (
            f"Moderate risk indicators detected. Community awareness recommended around '{primary_concern}'."
        )
    else:
        analysis = "Low risk indicators detected. Area has minimal reported incidents."

    return {
        "area": area_name,
        "total_reports": len(area_reports),
        "category_counts": cat_counts,
        "severity_counts": sev_counts,
        "highest_severity": highest_sev,
        "total_confirmations": total_confirmations,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "primary_concern": primary_concern,
        "analysis": analysis,
        "breakdown": {
            "severity_pts": severity_pts,
            "frequency_pts": frequency_pts,
            "confirmation_pts": confirmation_pts
        }
    }


def display_area_risk(area_name):
    """Prints a structured risk report for an area."""
    res = calculate_area_risk(area_name)

    print("\n" + "=" * 58)
    print(f"  SAFETY RISK ANALYSIS (ACADEMIC RULE-BASED PROTOTYPE)")
    print("=" * 58)
    print(f"  Target Area: {res['area']}")
    print(f"  Total Reports: {res['total_reports']}")

    if res['category_counts']:
        print("  Reports by Category:")
        for cat, cnt in res['category_counts'].items():
            print(f"    - {cat}: {cnt}")

    print(f"\n  Highest Severity Observed: {res['highest_severity']}")
    print(f"  Total Community Confirmations: {res['total_confirmations']}")
    print("-" * 58)
    print(f"  Calculated Risk Score: {res['risk_score']}/100")
    print(f"  Risk Classification  : [{res['risk_level']}]")
    print(f"  Primary Concern      : {res['primary_concern']}")
    print(f"\n  Analysis & Insights:")
    print(f"  {res['analysis']}")
    print("-" * 58)
    print("  Score Formula Breakdown:")
    print(f"    - Severity Contribution    : {res['breakdown']['severity_pts']}/50 pts")
    print(f"    - Frequency Contribution   : {res['breakdown']['frequency_pts']}/30 pts")
    print(f"    - Confirmation Contribution: {res['breakdown']['confirmation_pts']}/20 pts")
    print("=" * 58)
    print("  [Note: Academic prototype calculation for demonstration purposes.]")


def analyze_all_known_areas():
    """Calculates and displays risk scores for all unique areas currently in reports."""
    reports = load_json(REPORTS_FILE, default=[])
    if not reports:
        print("  No safety reports available to analyze.")
        return

    unique_areas = sorted(list(set(r.get("area", "").strip() for r in reports if r.get("area"))))
    print(f"\nEvaluating Risk across {len(unique_areas)} known area(s):\n")

    print(f"  {'Area Name':<18} | {'Reports':<8} | {'Score':<8} | {'Risk Level':<12} | {'Primary Issue'}")
    print("  " + "-" * 64)

    for area in unique_areas:
        info = calculate_area_risk(area)
        lvl = info["risk_level"]
        lvl_tag = f"🔴 {lvl}" if lvl == "HIGH" else (f"🟡 {lvl}" if lvl == "MEDIUM" else f"🟢 {lvl}")
        print(f"  {info['area']:<18} | {info['total_reports']:<8} | {info['risk_score']:>3}/100  | {lvl_tag:<14} | {info['primary_concern']}")


def risk_analyzer_interactive():
    """Interactive console sub-menu for Module 4."""
    while True:
        print_section("Module 4: Rule-Based Safety Risk Analyzer")
        print("  [1] Analyze Specific Area by Name")
        print("  [2] View Comparative Safety Overview of All Areas")
        print("  [0] Return to Main Menu")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            print_section("Area Risk Analysis")
            area = input("Enter Area Name (e.g., Campus Gate, Hostel Road): ").strip()
            if area:
                display_area_risk(area)
            else:
                print("\n[!] Area name cannot be empty.")

        elif choice == "2":
            print_section("Comparative Area Safety Overview")
            analyze_all_known_areas()

        elif choice == "0":
            break
        else:
            print("\n[!] Invalid selection. Please enter a valid number.")
