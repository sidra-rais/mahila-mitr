"""
Module 5 — Community Safety Analytics
Computes aggregate statistical summaries from live stored JSON data without hard-coded numbers.
"""

from storage import load_json
from utils import print_section


def generate_community_analytics():
    """
    Computes and returns a dictionary of aggregate analytics derived from stored data.
    """
    reports = load_json("safety_reports.json", default=[])
    help_reqs = load_json("help_requests.json", default=[])
    mitrs = load_json("mahila_mitrs.json", default=[])

    # 1. Reports Analytics
    total_reports = len(reports)
    sev_counts = {"High": 0, "Medium": 0, "Low": 0}
    cat_counts = {}
    area_counts = {}
    total_confirmations = 0

    for r in reports:
        sev = r.get("severity", "Medium")
        if sev in sev_counts:
            sev_counts[sev] += 1

        cat = r.get("category", "Other")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

        area = r.get("area", "Unknown")
        area_counts[area] = area_counts.get(area, 0) + 1

        total_confirmations += int(r.get("confirmations", 1))

    most_reported_issue = max(cat_counts.items(), key=lambda x: x[1])[0] if cat_counts else "None"
    most_reported_area = max(area_counts.items(), key=lambda x: x[1])[0] if area_counts else "None"

    # 2. Help Request Analytics
    total_help = len(help_reqs)
    resolved_help = sum(1 for h in help_reqs if h.get("status", "").lower() == "resolved")
    pending_help = sum(1 for h in help_reqs if h.get("status", "").lower() == "pending")

    resolution_rate = (resolved_help / total_help * 100) if total_help > 0 else 0.0

    # 3. Mahila Mitr Volunteer Analytics
    total_mitrs = len(mitrs)
    available_mitrs = sum(1 for m in mitrs if m.get("is_available", True))
    busy_mitrs = total_mitrs - available_mitrs
    availability_rate = (available_mitrs / total_mitrs * 100) if total_mitrs > 0 else 0.0

    return {
        "total_reports": total_reports,
        "high_severity_reports": sev_counts["High"],
        "medium_severity_reports": sev_counts["Medium"],
        "low_severity_reports": sev_counts["Low"],
        "most_reported_issue": most_reported_issue,
        "most_reported_area": most_reported_area,
        "total_confirmations": total_confirmations,
        "total_help_requests": total_help,
        "resolved_help_requests": resolved_help,
        "pending_help_requests": pending_help,
        "resolution_rate": round(resolution_rate, 1),
        "total_mitrs": total_mitrs,
        "available_mitrs": available_mitrs,
        "busy_mitrs": busy_mitrs,
        "availability_rate": round(availability_rate, 1)
    }


def display_community_summary():
    """Prints a structured Community Safety Summary in the console."""
    data = generate_community_analytics()

    print("\n" + "=" * 58)
    print("  🌸 COMMUNITY SAFETY SUMMARY & ANALYTICS 🌸")
    print("=" * 58)
    print("  📍 SAFETY REPORTS OVERVIEW:")
    print(f"     Total Safety Reports Submitted : {data['total_reports']}")
    print(f"       - High Severity              : {data['high_severity_reports']}")
    print(f"       - Medium Severity            : {data['medium_severity_reports']}")
    print(f"       - Low Severity               : {data['low_severity_reports']}")
    print(f"     Most Frequently Reported Issue : {data['most_reported_issue']}")
    print(f"     Highest Incident Area          : {data['most_reported_area']}")
    print(f"     Total Community Confirmations  : {data['total_confirmations']}")

    print("\n  🆘 HELP REQUEST PERFORMANCE:")
    print(f"     Total Help Requests Logged     : {data['total_help_requests']}")
    print(f"       - Resolved Requests          : {data['resolved_help_requests']}")
    print(f"       - Pending Active Requests    : {data['pending_help_requests']}")
    print(f"     Assistance Resolution Rate     : {data['resolution_rate']}%")

    print("\n  🤝 MAHILA MITR VOLUNTEER NETWORK:")
    print(f"     Total Registered Mitrs         : {data['total_mitrs']}")
    print(f"       - Active / Available Now     : {data['available_mitrs']}")
    print(f"       - Currently Busy             : {data['busy_mitrs']}")
    print(f"     Volunteer Availability Rate    : {data['availability_rate']}%")
    print("=" * 58)
    print("  [Statistics dynamically computed from live storage data]")


def analytics_interactive():
    """Interactive console entry for Module 5."""
    print_section("Module 5: Community Safety Analytics")
    display_community_summary()
    input("\nPress Enter to return to main menu...")
