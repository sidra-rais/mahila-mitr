"""
Validation Module for Mahila Mitr System
Contains reusable validation helper functions.
"""

ALLOWED_ASSISTANCE_TYPES = [
    "Emotional support",
    "Accompaniment/support",
    "Navigation help",
    "Safe-place guidance",
    "General assistance"
]

ALLOWED_SITUATIONS = [
    "Stranded",
    "Feeling unsafe",
    "Need navigation assistance",
    "Need someone to accompany/support",
    "Need a safe public place",
    "Other"
]

ALLOWED_URGENCY_LEVELS = ["Low", "Medium", "High"]

ALLOWED_REPORT_CATEGORIES = [
    "Poor lighting",
    "Harassment concern",
    "Isolated area",
    "Unsafe road/path",
    "Suspicious activity",
    "Other"
]

ALLOWED_SEVERITY_LEVELS = ["Low", "Medium", "High"]


def validate_non_empty(text, field_name="Field"):
    """Checks if a string is non-empty after stripping whitespace."""
    if not text or not str(text).strip():
        return False, f"{field_name} cannot be empty."
    return True, ""


def validate_choice(value, allowed_list, field_name="Selection"):
    """Checks if a value is present within an allowed list (case-insensitive check)."""
    if not value:
        return False, f"{field_name} is required."
    for item in allowed_list:
        if item.lower() == str(value).strip().lower():
            return True, item
    options_str = ", ".join(allowed_list)
    return False, f"Invalid {field_name}. Must be one of: {options_str}"


def validate_id_format(entity_id, prefix=""):
    """Validates simple ID non-emptiness and optional prefix format."""
    is_valid, msg = validate_non_empty(entity_id, "ID")
    if not is_valid:
        return False, msg
    if prefix and not str(entity_id).upper().startswith(prefix.upper()):
        return False, f"ID should start with '{prefix}' (e.g., {prefix}01)."
    return True, ""


def validate_positive_integer(val, field_name="Number"):
    """Validates that a value is a non-negative integer."""
    try:
        num = int(val)
        if num < 0:
            return False, f"{field_name} cannot be negative."
        return True, num
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid integer."
