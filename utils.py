"""
Utilities Module for Mahila Mitr System
Provides formatting, timestamp helpers, and UI display helpers for the console.
"""

from datetime import datetime


def get_current_timestamp():
    """Returns the current date and time as a readable string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def print_banner(title, subtitle=""):
    """Prints a clean decorative banner in the console."""
    print("\n" + "=" * 62)
    print(f"  🌸 {title.center(54)} 🌸")
    if subtitle:
        print(f"  {subtitle.center(58)}")
    print("=" * 62)


def print_section(title):
    """Prints a section header."""
    print(f"\n--- {title} " + "-" * max(2, 54 - len(title)))


def prompt_menu_choice(options_dict, prompt_text="Choose an option: "):
    """
    Displays a numbered menu dictionary and prompts for a valid choice.
    options_dict: { '1': 'Option label', ... }
    """
    for key, label in options_dict.items():
        print(f"  [{key}] {label}")
    choice = input(f"\n{prompt_text}").strip()
    return choice
