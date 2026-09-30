"""
Module 3 — Safety Report Management
Handles full CRUD operations, category filtering, search, and community confirmations for location reports.
"""

from models import SafetyReport
from storage import load_json, save_json
from validation import (
    ALLOWED_REPORT_CATEGORIES,
    ALLOWED_SEVERITY_LEVELS,
    validate_choice,
    validate_id_format,
    validate_non_empty,
    validate_positive_integer,
)
from utils import get_current_timestamp, print_section

REPORTS_FILE = "safety_reports.json"


def get_all_reports():
    """Loads all safety reports from storage."""
    return load_json(REPORTS_FILE, default=[])


def save_all_reports(reports_list):
    """Saves safety reports to storage."""
    return save_json(REPORTS_FILE, reports_list)


def add_safety_report(report_id, area, category, severity, description):
    """
    Validates and adds a new Safety Report.
    """
    valid_id, id_err = validate_id_format(report_id, prefix="REP")
    if not valid_id:
        return False, id_err

    valid_area, area_err = validate_non_empty(area, "Area/Location")
    if not valid_area:
        return False, area_err

    valid_cat, cat_val = validate_choice(category, ALLOWED_REPORT_CATEGORIES, "Issue Category")
    if not valid_cat:
        return False, cat_val

    valid_sev, sev_val = validate_choice(severity, ALLOWED_SEVERITY_LEVELS, "Severity Level")
    if not valid_sev:
        return False, sev_val

    valid_desc, desc_err = validate_non_empty(description, "Description")
    if not valid_desc:
        return False, desc_err

    reports = get_all_reports()
    for r in reports:
        if r.get("id", "").upper() == str(report_id).strip().upper():
            return False, f"Report with ID '{report_id}' already exists."

    new_report = SafetyReport(
        report_id=report_id.strip().upper(),
        area=area.strip(),
        category=cat_val,
        severity=sev_val,
        description=description.strip(),
        date_time=get_current_timestamp(),
        confirmations=1,
        status="Reported"
    )

    reports.append(new_report.to_dict())
    save_all_reports(reports)
    return True, f"Safety Report '{new_report.id}' registered successfully for '{area}'."


def list_reports(filtered_list=None):
    """Prints safety reports in a clean format."""
    reports = filtered_list if filtered_list is not None else get_all_reports()
    if not reports:
        print("  No safety reports found.")
        return

    for r in reports:
        sev = r.get("severity", "Medium")
        sev_tag = "🔴 High" if sev == "High" else ("🟡 Medium" if sev == "Medium" else "🟢 Low")
        status_tag = f"[{r.get('status', 'Reported')}]"

        print(f"  Report ID: {r.get('id'):<8} | Area: {r.get('area'):<16} | Status: {status_tag:<12}")
        print(f"  Category : {r.get('category'):<16} | Severity: {sev_tag:<14} | Confirmations: {r.get('confirmations', 1)}")
        print(f"  Reported : {r.get('date_time')} | Details: {r.get('description')}")
        print("  " + "-" * 58)


def filter_reports(area=None, category=None, severity=None):
    """Filters safety reports by area, category, or severity."""
    reports = get_all_reports()
    results = []
    for r in reports:
        if area and area.strip().lower() not in r.get("area", "").lower():
            continue
        if category and category.strip().lower() != r.get("category", "").lower():
            continue
        if severity and severity.strip().lower() != r.get("severity", "").lower():
            continue
        results.append(r)
    return results


def confirm_safety_report(report_id):
    """
    Increments community confirmation count on a report.
    Automatically marks status as 'Verified' when confirmations reach >= 3.
    """
    reports = get_all_reports()
    found = False
    new_count = 0
    new_status = ""

    for r in reports:
        if r.get("id", "").upper() == str(report_id).strip().upper():
            r["confirmations"] = r.get("confirmations", 1) + 1
            new_count = r["confirmations"]
            if new_count >= 3:
                r["status"] = "Verified"
            new_status = r["status"]
            found = True
            break

    if not found:
        return False, f"Report ID '{report_id}' not found."

    save_all_reports(reports)
    return True, f"Report {report_id} confirmed! Total confirmations: {new_count} (Status: {new_status})."


def delete_safety_report(report_id):
    """Deletes a safety report by ID."""
    reports = get_all_reports()
    initial_len = len(reports)
    reports = [r for r in reports if r.get("id", "").upper() != str(report_id).strip().upper()]

    if len(reports) == initial_len:
        return False, f"Report ID '{report_id}' not found."

    save_all_reports(reports)
    return True, f"Safety Report '{report_id}' deleted successfully."


def update_safety_report_desc(report_id, new_description):
    """Updates the description on an existing report."""
    valid_desc, desc_err = validate_non_empty(new_description, "Description")
    if not valid_desc:
        return False, desc_err

    reports = get_all_reports()
    found = False
    for r in reports:
        if r.get("id", "").upper() == str(report_id).strip().upper():
            r["description"] = new_description.strip()
            found = True
            break

    if not found:
        return False, f"Report ID '{report_id}' not found."

    save_all_reports(reports)
    return True, f"Description for report '{report_id}' updated successfully."


def manage_safety_reports_interactive():
    """Interactive console sub-menu for Module 3."""
    while True:
        print_section("Module 3: Safety Report Management")
        print("  [1] View All Safety Reports")
        print("  [2] Submit New Safety Report")
        print("  [3] Confirm a Safety Report (Community Verification)")
        print("  [4] Filter Reports by Area / Category / Severity")
        print("  [5] Update Safety Report Description")
        print("  [6] Delete Safety Report")
        print("  [0] Return to Main Menu")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            print_section("All Safety Reports")
            list_reports()

        elif choice == "2":
            print_section("Submit New Safety Report")
            rep_id = input("Enter Report ID (e.g. REP208): ").strip()
            area = input("Enter Area/Location: ").strip()

            print("\nCategories:")
            for idx, opt in enumerate(ALLOWED_REPORT_CATEGORIES, start=1):
                print(f"  [{idx}] {opt}")
            cat_choice = input("Select Category (1-6): ").strip()
            if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(ALLOWED_REPORT_CATEGORIES):
                category = ALLOWED_REPORT_CATEGORIES[int(cat_choice) - 1]
            else:
                category = cat_choice

            print("\nSeverity Levels:")
            for idx, opt in enumerate(ALLOWED_SEVERITY_LEVELS, start=1):
                print(f"  [{idx}] {opt}")
            sev_choice = input("Select Severity (1-3): ").strip()
            if sev_choice.isdigit() and 1 <= int(sev_choice) <= len(ALLOWED_SEVERITY_LEVELS):
                severity = ALLOWED_SEVERITY_LEVELS[int(sev_choice) - 1]
            else:
                severity = sev_choice

            description = input("Enter Details/Description: ").strip()

            success, msg = add_safety_report(rep_id, area, category, severity, description)
            print(f"\n=> {msg}")

        elif choice == "3":
            print_section("Community Confirmation")
            rep_id = input("Enter Report ID to confirm (e.g. REP204): ").strip()
            success, msg = confirm_safety_report(rep_id)
            print(f"\n=> {msg}")

        elif choice == "4":
            print_section("Filter Reports")
            print("Leave blank if you do not want to filter by that criteria.")
            area_input = input("Filter by Area (e.g. Campus Gate): ").strip()
            cat_input = input("Filter by Category (e.g. Poor lighting): ").strip()
            sev_input = input("Filter by Severity (Low/Medium/High): ").strip()

            filtered = filter_reports(
                area=area_input if area_input else None,
                category=cat_input if cat_input else None,
                severity=sev_input if sev_input else None
            )
            print(f"\nMatching Results ({len(filtered)} found):")
            list_reports(filtered)

        elif choice == "5":
            print_section("Update Report Description")
            rep_id = input("Enter Report ID: ").strip()
            new_desc = input("Enter Updated Description: ").strip()
            success, msg = update_safety_report_desc(rep_id, new_desc)
            print(f"\n=> {msg}")

        elif choice == "6":
            print_section("Delete Safety Report")
            rep_id = input("Enter Report ID to delete: ").strip()
            confirm_del = input(f"Are you sure you want to delete {rep_id}? (y/n): ").strip().lower()
            if confirm_del == "y":
                success, msg = delete_safety_report(rep_id)
                print(f"\n=> {msg}")
            else:
                print("\n=> Deletion cancelled.")

        elif choice == "0":
            break
        else:
            print("\n[!] Invalid selection. Please enter a valid number.")
