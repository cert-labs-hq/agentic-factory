import unittest
import json
from pathlib import Path
import sys
import os

# Add src to path to allow importing from BKP_004
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.registry_generator import SliceValidator

class TestSliceValidator(unittest.TestCase):
    def setUp(self):
        self.schema_path = Path(".factory/contracts/schema_file.json")
        self.validator = SliceValidator(self.schema_path)

    def test_validator_initialization(self):
        self.assertIsNotNone(self.validator)

    def test_validate_valid_slice(self):
        valid_slice = {
            "id": "TST-001",
            "title": "Test Slice",
            "status": "Planned",
            "created_at": "2026-05-07T12:00:00Z",
            "updated_at": "2026-05-07T12:00:00Z",
            "assigned_to": "tester",
            "spec_path": "docs/specs/test.md",
            "dependencies": [],
            "metadata_version": "1.0"
        }
        # This should fail (Red phase) because implementation is 'pass' and default return is None
        self.assertTrue(self.validator.validate(valid_slice))

    def test_validate_invalid_slice(self):
        invalid_slice = {
            "id": "TST-001"
            # Missing required fields
        }
        self.assertFalse(self.validator.validate(invalid_slice))

if __name__ == '__main__':
    unittest.main()
