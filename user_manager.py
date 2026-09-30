"""
Module 1 — User & Mahila Mitr Management
Handles registration, viewing, searching, and updating availability for Mahila Mitrs and Users.
"""

from models import MahilaMitr, User
from storage import load_json, save_json
from validation import (
    ALLOWED_ASSISTANCE_TYPES,
    validate_choice,
    validate_id_format,
    validate_non_empty,
)
from utils import print_section

MITRS_FILE = "mahila_mitrs.json"
USERS_FILE = "users.json"


def get_all_mitrs():
    """Loads all Mahila Mitrs from storage as a list of dicts."""
    return load_json(MITRS_FILE, default=[])


def save_all_mitrs(mitrs_list):
    """Saves the list of Mahila Mitr dicts into storage."""
    return save_json(MITRS_FILE, mitrs_list)


def register_mahila_mitr(mitr_id, name, area, assistance_type, phone_demo="N/A"):
    """
    Registers a new Mahila Mitr volunteer.
    Validates inputs and prevents duplicate IDs.
    """
    valid_id, id_err = validate_id_format(mitr_id, prefix="MM")
    if not valid_id:
        return False, id_err

    valid_name, name_err = validate_non_empty(name, "Name")
    if not valid_name:
        return False, name_err

    valid_area, area_err = validate_non_empty(area, "Area/Location")
    if not valid_area:
        return False, area_err

    valid_type, type_val = validate_choice(assistance_type, ALLOWED_ASSISTANCE_TYPES, "Assistance Type")
    if not valid_type:
        return False, type_val

    mitrs = get_all_mitrs()
    for m in mitrs:
        if m.get("id", "").upper() == str(mitr_id).strip().upper():
            return False, f"Mahila Mitr with ID '{mitr_id}' already exists."

    new_mitr = MahilaMitr(
        mitr_id=mitr_id.strip().upper(),
        name=name.strip(),
        area=area.strip(),
        is_available=True,
        assistance_type=type_val,
        phone_demo=phone_demo.strip() if phone_demo else "N/A",
        help_count=0
    )

    mitrs.append(new_mitr.to_dict())
    save_all_mitrs(mitrs)
    return True, f"Mahila Mitr '{name}' registered successfully with ID {new_mitr.id}."


def list_mahila_mitrs(filter_available_only=False):
    """Displays all Mahila Mitrs in a readable console format."""
    mitrs = get_all_mitrs()
    if not mitrs:
        print("  No Mahila Mitrs found in the system.")
        return

    count = 0
    for m in mitrs:
        if filter_available_only and not m.get("is_available", True):
            continue

        status_tag = "🟢 Available" if m.get("is_available", True) else "🔴 Busy/Unavailable"
        print(f"  ID: {m.get('id', 'N/A'):<6} | Name: {m.get('name', 'N/A'):<16} | Area: {m.get('area', 'N/A'):<14}")
        print(f"         Status: {status_tag:<18} | Type: {m.get('assistance_type', 'General')}")
        print(f"         Assisted: {m.get('help_count', 0)} times | Contact: {m.get('phone_demo', 'N/A')}")
        print("  " + "-" * 58)
        count += 1

    if count == 0 and filter_available_only:
        print("  No currently available Mahila Mitrs found.")


def search_mahila_mitrs(query):
    """Searches Mahila Mitrs by name, area, or assistance type."""
    mitrs = get_all_mitrs()
    if not query or not query.strip():
        return []

    q = query.strip().lower()
    results = []
    for m in mitrs:
        name_match = q in m.get("name", "").lower()
        area_match = q in m.get("area", "").lower()
        type_match = q in m.get("assistance_type", "").lower()
        if name_match or area_match or type_match:
            results.append(m)
    return results


def toggle_mitr_availability(mitr_id):
    """Toggles a Mahila Mitr's availability between Available and Busy."""
    mitrs = get_all_mitrs()
    found = False
    new_status = False

    for m in mitrs:
        if m.get("id", "").upper() == str(mitr_id).strip().upper():
            m["is_available"] = not m.get("is_available", True)
            new_status = m["is_available"]
            found = True
            break

    if not found:
        return False, f"No Mahila Mitr found with ID '{mitr_id}'."

    save_all_mitrs(mitrs)
    status_str = "Available" if new_status else "Busy/Unavailable"
    return True, f"Status updated: Mahila Mitr {mitr_id} is now '{status_str}'."


def update_mitr_assistance_type(mitr_id, new_assistance_type):
    """Updates the assistance specialization of a Mahila Mitr."""
    valid_type, type_val = validate_choice(new_assistance_type, ALLOWED_ASSISTANCE_TYPES, "Assistance Type")
    if not valid_type:
        return False, type_val

    mitrs = get_all_mitrs()
    found = False
    for m in mitrs:
        if m.get("id", "").upper() == str(mitr_id).strip().upper():
            m["assistance_type"] = type_val
            found = True
            break

    if not found:
        return False, f"No Mahila Mitr found with ID '{mitr_id}'."

    save_all_mitrs(mitrs)
    return True, f"Assistance type updated to '{type_val}' for ID {mitr_id}."


def manage_mitrs_interactive():
    """Interactive sub-menu for Mahila Mitr management in console."""
    while True:
        print_section("Module 1: Mahila Mitr Management")
        print("  [1] View All Mahila Mitrs")
        print("  [2] View Available Mahila Mitrs Only")
        print("  [3] Register New Mahila Mitr")
        print("  [4] Search Mahila Mitrs")
        print("  [5] Toggle Availability Status (Available / Busy)")
        print("  [6] Update Assistance Type")
        print("  [0] Return to Main Menu")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            print_section("All Registered Mahila Mitrs")
            list_mahila_mitrs(filter_available_only=False)

        elif choice == "2":
            print_section("Currently Available Mahila Mitrs")
            list_mahila_mitrs(filter_available_only=True)

        elif choice == "3":
            print_section("Register New Mahila Mitr")
            mitr_id = input("Enter Mitr ID (e.g., MM07): ").strip()
            name = input("Enter Full Name: ").strip()
            area = input("Enter Area/Location (e.g. Campus Gate, Hostel Road): ").strip()

            print("\nAllowed Assistance Types:")
            for idx, opt in enumerate(ALLOWED_ASSISTANCE_TYPES, start=1):
                print(f"  [{idx}] {opt}")
            type_choice = input("Select Assistance Type (1-5 or type name): ").strip()

            if type_choice.isdigit() and 1 <= int(type_choice) <= len(ALLOWED_ASSISTANCE_TYPES):
                asst_type = ALLOWED_ASSISTANCE_TYPES[int(type_choice) - 1]
            else:
                asst_type = type_choice

            phone = input("Enter Demo Contact Phone (or press Enter): ").strip()
            success, msg = register_mahila_mitr(mitr_id, name, area, asst_type, phone)
            print(f"\n=> {msg}")

        elif choice == "4":
            print_section("Search Mahila Mitrs")
            q = input("Enter search query (name, area, or assistance type): ").strip()
            results = search_mahila_mitrs(q)
            if results:
                print(f"\nFound {len(results)} matching record(s):")
                for m in results:
                    status_tag = "🟢 Available" if m.get("is_available", True) else "🔴 Busy"
                    print(f"  - [{m.get('id')}] {m.get('name')} | {m.get('area')} | {status_tag} | {m.get('assistance_type')}")
            else:
                print(f"\n=> No matching Mahila Mitrs found for query '{q}'.")

        elif choice == "5":
            print_section("Toggle Availability")
            mitr_id = input("Enter Mahila Mitr ID: ").strip()
            success, msg = toggle_mitr_availability(mitr_id)
            print(f"\n=> {msg}")

        elif choice == "6":
            print_section("Update Assistance Type")
            mitr_id = input("Enter Mahila Mitr ID: ").strip()
            print("\nAllowed Assistance Types:")
            for idx, opt in enumerate(ALLOWED_ASSISTANCE_TYPES, start=1):
                print(f"  [{idx}] {opt}")
            type_choice = input("Select New Assistance Type: ").strip()
            if type_choice.isdigit() and 1 <= int(type_choice) <= len(ALLOWED_ASSISTANCE_TYPES):
                new_type = ALLOWED_ASSISTANCE_TYPES[int(type_choice) - 1]
            else:
                new_type = type_choice

            success, msg = update_mitr_assistance_type(mitr_id, new_type)
            print(f"\n=> {msg}")

        elif choice == "0":
            break
        else:
            print("\n[!] Invalid selection. Please enter a valid number.")
