import unittest
import json
import os
import shutil
from pathlib import Path
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.registry_generator import RegistryAggregator, SliceValidator

class TestRegistryAggregator(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("tests/BKP-004/tmp_slices")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.schema_path = Path(".factory/contracts/schema_file.json")
        self.validator = SliceValidator(self.schema_path)
        
        # Create valid dummy slices
        self.create_slice("ABC-001.json", {"id": "ABC-001", "status": "Planned", "total_tokens": 1000})
        self.create_slice("XYZ-123.json", {"id": "XYZ-123", "status": "Warehoused", "total_tokens": 5000})
        # Create invalid filename
        self.create_slice("not-a-slice.json", {"id": "BAD", "status": "Planned"})
        
        self.aggregator = RegistryAggregator(self.test_dir, self.validator)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def create_slice(self, filename, data):
        # Add required fields for validator
        full_data = {
            "title": "Test",
            "created_at": "2026-05-07T12:00:00Z",
            "updated_at": "2026-05-07T12:00:00Z",
            "assigned_to": "tester",
            "spec_path": "docs/specs/test.md",
            "dependencies": [],
            "metadata_version": "1.0"
        }
        full_data.update(data)
        with open(self.test_dir / filename, 'w') as f:
            json.dump(full_data, f)

    def test_discover_slices(self):
        # Should only find ABC-001 and XYZ-123
        slices = self.aggregator.discover_slices()
        self.assertEqual(len(slices), 2)
        filenames = [s.name for s in slices]
        self.assertIn("ABC-001.json", filenames)
        self.assertIn("XYZ-123.json", filenames)
        self.assertNotIn("not-a-slice.json", filenames)

    def test_aggregate_metrics(self):
        registry = self.aggregator.aggregate()
        metadata = registry.get("metadata", {})
        self.assertEqual(metadata.get("total_slices"), 2)
        status_summary = metadata.get("status_summary", {})
        self.assertEqual(status_summary.get("Planned"), 1)
        self.assertEqual(status_summary.get("Warehoused"), 1)

if __name__ == '__main__':
    unittest.main()
