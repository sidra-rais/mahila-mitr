"""
Storage Module for Mahila Mitr System
Handles reading and writing JSON data files with proper error handling.
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def get_file_path(filename):
    """Returns absolute path for a data file."""
    return os.path.join(DATA_DIR, filename)


def load_json(filename, default=None):
    """
    Safely load data from a JSON file.
    Returns default if file is missing or corrupted.
    """
    if default is None:
        default = []

    filepath = get_file_path(filename)
    if not os.path.exists(filepath):
        return default

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as err:
        print(f"[Warning] Failed to read {filename}: {err}. Using default.")
        return default


def save_json(filename, data):
    """
    Safely save data into a JSON file.
    Creates the directory if it doesn't exist.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = get_file_path(filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as err:
        print(f"[Error] Failed to write {filename}: {err}")
        return False
