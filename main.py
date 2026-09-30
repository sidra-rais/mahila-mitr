"""
🌸 MAHILA MITR — Community Safety Assistance & Risk Analysis System
Main Console Application Entry Point
Course Project submission for VITyarthi — Build Your Own Project.
"""

import sys
from user_manager import manage_mitrs_interactive
from help_request import manage_help_requests_interactive
from safety_reports import manage_safety_reports_interactive
from risk_analyzer import risk_analyzer_interactive
from analytics import analytics_interactive
from utils import print_banner, print_section


def display_main_menu():
    """Prints the main interactive menu."""
    print_banner("MAHILA MITR", "Community Safety Assistance & Risk Analysis System")
    print("  [1] 👥 Manage Mahila Mitrs (Register, View, Availability)")
    print("  [2] 🆘 Help Requests & Smart Matching Algorithm")
    print("  [3] 📍 Safety Report Management & Confirmations (CRUD)")
    print("  [4] 🛡️ Rule-Based Area Safety Risk Analyzer")
    print("  [5] 📊 Community Safety Analytics & Statistical Summary")
    print("  [6] ℹ️ About Project & Academic Prototype Information")
    print("  [0] 🚪 Exit Application")
    print("=" * 62)


def display_about_info():
    """Displays project background, architecture, and academic disclaimer."""
    print_section("About Mahila Mitr Academic Prototype")
    print("""
  Title: MAHILA MITR — Community Safety Assistance & Risk Analysis System
  Tagline: "Women supporting women, wherever you need it."
  
  Concept Overview:
  Mahila Mitr is a modular Python-based prototype designed to explore
  how community-driven solidarity, decentralized reporting, and rule-based
  risk analysis can support women in non-emergency safety situations.

  Core Modules:
    1. Mahila Mitr Management  : Volunteer registry & availability control.
    2. Help Request & Matching : Rule-based multi-factor suitability scoring.
    3. Safety Reports          : Community hazard reporting & verification.
    4. Safety Risk Analyzer    : Transparent weighted 0-100 risk scoring.
    5. Community Analytics     : Real-time statistical insights from data.

  Academic Disclaimer:
  ----------------------------------------------------------------------
  This software is an educational prototype developed for B.Tech CSE.
  It does NOT replace official emergency response systems.
  In case of an immediate life-safety emergency, dial 112 or 181.
  ----------------------------------------------------------------------
    """)
    input("Press Enter to return to main menu...")


def main():
    """Main execution loop for the Mahila Mitr application."""
    while True:
        try:
            display_main_menu()
            choice = input("\nEnter your choice [0-6]: ").strip()

            if choice == "1":
                manage_mitrs_interactive()

            elif choice == "2":
                manage_help_requests_interactive()

            elif choice == "3":
                manage_safety_reports_interactive()

            elif choice == "4":
                risk_analyzer_interactive()

            elif choice == "5":
                analytics_interactive()

            elif choice == "6":
                display_about_info()

            elif choice == "0":
                print("\n" + "=" * 62)
                print("  Thank you for using 🌸 Mahila Mitr.")
                print("  Empowering safer communities together.")
                print("=" * 62 + "\n")
                sys.exit(0)

            else:
                print("\n[!] Invalid option. Please choose a number between 0 and 6.")
                input("Press Enter to continue...")

        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user. Exiting cleanly...")
            break
        except Exception as e:
            print(f"\n[Unexpected Error] An issue occurred: {e}")
            input("Press Enter to return to main menu...")


if __name__ == "__main__":
    main()
