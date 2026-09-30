"""
Unit Tests for Mahila Mitr Python System
Uses standard Python unittest library to verify all 5 functional modules.
"""

import os
import sys
import unittest

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import MahilaMitr, HelpRequest, SafetyReport
from validation import (
    validate_non_empty,
    validate_choice,
    validate_id_format,
    ALLOWED_ASSISTANCE_TYPES,
    ALLOWED_SEVERITY_LEVELS
)
from matching import calculate_match_score, find_suitable_mitrs
from risk_analyzer import calculate_area_risk
from analytics import generate_community_analytics
from user_manager import get_all_mitrs
from safety_reports import get_all_reports


class TestMahilaMitrSystem(unittest.TestCase):
    """Test suite covering core logic, matching algorithms, risk scoring, and validation."""

    def test_validation_non_empty(self):
        """Test non-empty string validation helper."""
        is_valid, msg = validate_non_empty("Campus Gate", "Area")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")

        is_invalid, err_msg = validate_non_empty("   ", "Area")
        self.assertFalse(is_invalid)
        self.assertIn("cannot be empty", err_msg)

    def test_validation_choice(self):
        """Test allowed choices validation."""
        valid, val = validate_choice("High", ALLOWED_SEVERITY_LEVELS, "Severity")
        self.assertTrue(valid)
        self.assertEqual(val, "High")

        invalid, err = validate_choice("Critical", ALLOWED_SEVERITY_LEVELS, "Severity")
        self.assertFalse(invalid)
        self.assertIn("Invalid Severity", err)

    def test_validation_id_format(self):
        """Test ID format validation."""
        valid, msg = validate_id_format("MM01", prefix="MM")
        self.assertTrue(valid)

        invalid, msg = validate_id_format("REQ01", prefix="MM")
        self.assertFalse(invalid)

    def test_matching_algorithm_scoring(self):
        """Test rule-based smart matching calculation."""
        req = {
            "id": "REQ_TEST",
            "area": "Campus Gate",
            "urgency": "High",
            "assistance_needed": "Accompaniment/support"
        }

        # Perfect match candidate
        ideal_mitr = {
            "id": "MM_TEST1",
            "name": "Aanya",
            "area": "Campus Gate",
            "is_available": True,
            "assistance_type": "Accompaniment/support",
            "help_count": 5
        }

        score, reasons = calculate_match_score(req, ideal_mitr)
        # Expected: Available(30) + Same Area(40) + Skill Match(20) + High Urgency Bonus(10) = 100
        self.assertEqual(score, 100)

        # Unavailable candidate
        busy_mitr = {
            "id": "MM_TEST2",
            "name": "Riya",
            "area": "Campus Gate",
            "is_available": False,
            "assistance_type": "Accompaniment/support",
            "help_count": 2
        }
        busy_score, _ = calculate_match_score(req, busy_mitr)
        self.assertLess(busy_score, score)

    def test_risk_analyzer_calculation(self):
        """Test rule-based safety risk scoring and classification."""
        # Non-existent area should have score 0 and LOW risk
        empty_res = calculate_area_risk("NonExistentPlace")
        self.assertEqual(empty_res["risk_score"], 0)
        self.assertEqual(empty_res["risk_level"], "LOW")

        # Known area with High severity reports
        gate_res = calculate_area_risk("Campus Gate")
        self.assertGreater(gate_res["total_reports"], 0)
        self.assertIn(gate_res["risk_level"], ["LOW", "MEDIUM", "HIGH"])
        self.assertTrue(0 <= gate_res["risk_score"] <= 100)

    def test_community_analytics(self):
        """Test dynamic analytics generation."""
        stats = generate_community_analytics()
        self.assertIsInstance(stats["total_reports"], int)
        self.assertIsInstance(stats["total_help_requests"], int)
        self.assertIsInstance(stats["total_mitrs"], int)
        self.assertGreaterEqual(stats["resolution_rate"], 0.0)
        self.assertLessEqual(stats["resolution_rate"], 100.0)

    def test_models_serialization(self):
        """Test model class to_dict and from_dict methods."""
        mitr = MahilaMitr("MM99", "Test Name", "Test Area", True, "Navigation help", "12345", 2)
        d = mitr.to_dict()
        self.assertEqual(d["name"], "Test Name")

        mitr_recovered = MahilaMitr.from_dict(d)
        self.assertEqual(mitr_recovered.id, "MM99")
        self.assertEqual(mitr_recovered.assistance_type, "Navigation help")


if __name__ == "__main__":
    unittest.main(verbosity=2)
