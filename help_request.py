"""
Module 2 — Help Request Management & Interactive Matching
Handles creating requests, viewing request queues, matching with Mahila Mitrs, and resolving requests.
"""

from models import HelpRequest
from storage import load_json, save_json
from validation import (
    ALLOWED_ASSISTANCE_TYPES,
    ALLOWED_SITUATIONS,
    ALLOWED_URGENCY_LEVELS,
    validate_choice,
    validate_id_format,
    validate_non_empty,
)
from matching import find_suitable_mitrs
from utils import get_current_timestamp, print_section

HELP_FILE = "help_requests.json"


def get_all_help_requests():
    """Loads all help requests from storage."""
    return load_json(HELP_FILE, default=[])


def save_all_help_requests(requests_list):
    """Saves help requests into storage."""
    return save_json(HELP_FILE, requests_list)


def create_help_request(req_id, user_name, situation, area, urgency, assistance_needed, description):
    """
    Validates and creates a new Help Request in the system.
    """
    valid_id, id_err = validate_id_format(req_id, prefix="REQ")
    if not valid_id:
        return False, id_err

    valid_name, name_err = validate_non_empty(user_name, "User Name")
    if not valid_name:
        return False, name_err

    valid_sit, sit_val = validate_choice(situation, ALLOWED_SITUATIONS, "Situation")
    if not valid_sit:
        return False, sit_val

    valid_area, area_err = validate_non_empty(area, "Area/Location")
    if not valid_area:
        return False, area_err

    valid_urg, urg_val = validate_choice(urgency, ALLOWED_URGENCY_LEVELS, "Urgency Level")
    if not valid_urg:
        return False, urg_val

    valid_asst, asst_val = validate_choice(assistance_needed, ALLOWED_ASSISTANCE_TYPES, "Assistance Type")
    if not valid_asst:
        return False, asst_val

    valid_desc, desc_err = validate_non_empty(description, "Description")
    if not valid_desc:
        return False, desc_err

    requests = get_all_help_requests()
    for r in requests:
        if r.get("id", "").upper() == str(req_id).strip().upper():
            return False, f"Help Request ID '{req_id}' already exists."

    new_req = HelpRequest(
        req_id=req_id.strip().upper(),
        user_name=user_name.strip(),
        situation=sit_val,
        area=area.strip(),
        urgency=urg_val,
        assistance_needed=asst_val,
        description=description.strip(),
        status="Pending",
        assigned_mitr="None",
        created_at=get_current_timestamp()
    )

    requests.append(new_req.to_dict())
    save_all_help_requests(requests)
    return True, new_req.to_dict()


def display_matching_results(help_req_dict):
    """
    Runs the smart matching algorithm and prints formatted recommendation output.
    """
    print("\n" + "=" * 58)
    print(f"  HELP REQUEST #{help_req_dict.get('id')}")
    print("=" * 58)
    print(f"  User: {help_req_dict.get('user_name')}")
    print(f"  Situation: {help_req_dict.get('situation')}")
    print(f"  Area: {help_req_dict.get('area')}")
    print(f"  Urgency: {help_req_dict.get('urgency')}")
    print(f"  Assistance Needed: {help_req_dict.get('assistance_needed')}")
    print(f"  Description: {help_req_dict.get('description')}")
    print("-" * 58)

    matches = find_suitable_mitrs(help_req_dict, top_n=3)

    if not matches:
        print("  No registered Mahila Mitrs found to match.")
        print("=" * 58)
        return

    print("  SUITABLE MAHILA MITRS FOUND:\n")
    for idx, (mitr, score, reasons) in enumerate(matches, start=1):
        avail_str = "Available" if mitr.get("is_available", True) else "Busy"
        print(f"  {idx}. {mitr.get('name')}")
        print(f"     Area: {mitr.get('area')}")
        print(f"     Availability: {avail_str}")
        print(f"     Skill: {mitr.get('assistance_type')}")
        print(f"     Match Score: {score}/100")
        print(f"     Key Factors: {', '.join(reasons)}")
        print()

    best_match, best_score, best_reasons = matches[0]
    print("  RECOMMENDED MATCH:")
    print(f"  ⭐ {best_match.get('name')} (Score: {best_score}/100)")
    print(f"  Reason: Highest suitability based on availability, area and skill alignment.")
    print("=" * 58)


def list_help_requests(status_filter=None):
    """Displays all help requests in the console."""
    requests = get_all_help_requests()
    if not requests:
        print("  No help requests found in the system.")
        return

    count = 0
    for r in requests:
        if status_filter and r.get("status", "").lower() != status_filter.lower():
            continue

        status_tag = "🟡 Pending" if r.get("status") == "Pending" else "🟢 Resolved"
        urgency_tag = f"[{r.get('urgency')}]"
        print(f"  ID: {r.get('id'):<8} | User: {r.get('user_name'):<12} | Status: {status_tag:<12} | Urgency: {urgency_tag:<8}")
        print(f"  Situation: {r.get('situation')} at '{r.get('area')}' on {r.get('created_at')}")
        print(f"  Need: {r.get('assistance_needed')} | Assigned Mitr: {r.get('assigned_mitr')}")
        print(f"  Note: {r.get('description')}")
        print("  " + "-" * 58)
        count += 1

    if count == 0 and status_filter:
        print(f"  No requests found with status '{status_filter}'.")


def resolve_help_request(req_id, assigned_mitr_name):
    """Marks a help request as resolved and records assigned mitr."""
    requests = get_all_help_requests()
    found = False
    for r in requests:
        if r.get("id", "").upper() == str(req_id).strip().upper():
            r["status"] = "Resolved"
            r["assigned_mitr"] = assigned_mitr_name.strip() if assigned_mitr_name else "Community Mitr"
            found = True
            break

    if not found:
        return False, f"No help request found with ID '{req_id}'."

    save_all_help_requests(requests)
    return True, f"Request {req_id} marked as 'Resolved' with Mitr: {assigned_mitr_name}."


def manage_help_requests_interactive():
    """Interactive console sub-menu for Module 2."""
    while True:
        print_section("Module 2: Help Requests & Smart Matching")
        print("  [1] Create New Help Request")
        print("  [2] View All Help Requests")
        print("  [3] View Pending Help Requests Only")
        print("  [4] Find Smart Matches for Existing Request")
        print("  [5] Mark Help Request as Resolved")
        print("  [0] Return to Main Menu")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            print_section("Create New Help Request")
            req_id = input("Enter Request ID (e.g. REQ106): ").strip()
            name = input("Enter Your Name: ").strip()

            print("\nSituations:")
            for idx, opt in enumerate(ALLOWED_SITUATIONS, start=1):
                print(f"  [{idx}] {opt}")
            sit_choice = input("Select Situation (1-6 or type name): ").strip()
            if sit_choice.isdigit() and 1 <= int(sit_choice) <= len(ALLOWED_SITUATIONS):
                situation = ALLOWED_SITUATIONS[int(sit_choice) - 1]
            else:
                situation = sit_choice

            area = input("Enter Your Current Area/Location: ").strip()

            print("\nUrgency Levels:")
            for idx, opt in enumerate(ALLOWED_URGENCY_LEVELS, start=1):
                print(f"  [{idx}] {opt}")
            urg_choice = input("Select Urgency (1-3): ").strip()
            if urg_choice.isdigit() and 1 <= int(urg_choice) <= len(ALLOWED_URGENCY_LEVELS):
                urgency = ALLOWED_URGENCY_LEVELS[int(urg_choice) - 1]
            else:
                urgency = urg_choice

            print("\nAssistance Needed:")
            for idx, opt in enumerate(ALLOWED_ASSISTANCE_TYPES, start=1):
                print(f"  [{idx}] {opt}")
            asst_choice = input("Select Assistance Type (1-5): ").strip()
            if asst_choice.isdigit() and 1 <= int(asst_choice) <= len(ALLOWED_ASSISTANCE_TYPES):
                assistance = ALLOWED_ASSISTANCE_TYPES[int(asst_choice) - 1]
            else:
                assistance = asst_choice

            description = input("Enter Short Description of Situation: ").strip()

            success, res = create_help_request(req_id, name, situation, area, urgency, assistance, description)
            if success:
                print("\n[✓] Help Request Created Successfully!")
                display_matching_results(res)
            else:
                print(f"\n[!] Error: {res}")

        elif choice == "2":
            print_section("All Help Requests")
            list_help_requests()

        elif choice == "3":
            print_section("Pending Help Requests")
            list_help_requests(status_filter="Pending")

        elif choice == "4":
            print_section("Find Smart Matches for Request")
            req_id = input("Enter Request ID (e.g. REQ104): ").strip().upper()
            all_reqs = get_all_help_requests()
            target_req = None
            for r in all_reqs:
                if r.get("id", "").upper() == req_id:
                    target_req = r
                    break

            if target_req:
                display_matching_results(target_req)
            else:
                print(f"\n[!] Help Request with ID '{req_id}' not found.")

        elif choice == "5":
            print_section("Resolve Help Request")
            req_id = input("Enter Request ID to resolve: ").strip().upper()
            mitr_name = input("Enter Assigned Mahila Mitr Name: ").strip()
            success, msg = resolve_help_request(req_id, mitr_name)
            print(f"\n=> {msg}")

        elif choice == "0":
            break
        else:
            print("\n[!] Invalid selection. Please enter a valid number.")
