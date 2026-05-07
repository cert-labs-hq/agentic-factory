import unittest
import json
import os
from pathlib import Path
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.registry_generator import RegistryWriter

class TestRegistryWriter(unittest.TestCase):
    def setUp(self):
        self.output_path = Path("tests/BKP-004/index.json")
        self.aggregate_schema_path = Path(".factory/contracts/aggregate_slice_info.json")
        self.writer = RegistryWriter(self.output_path, self.aggregate_schema_path)

    def tearDown(self):
        if self.output_path.exists():
            os.remove(self.output_path)

    def test_write_registry(self):
        data = {
            "metadata": {
                "generated_at": "2026-05-07T12:00:00Z",
                "total_slices": 1,
                "status_summary": {
                    "Planned": 1, "Quota-Blocked": 0, "In Progress": 0,
                    "In Review": 0, "Approved": 0, "Warehoused": 0, "Rejected": 0
                },
                "global_finops": {
                    "total_combined_tokens": 1000,
                    "total_prompt_tokens": 0,
                    "total_reasoning_tokens": 0,
                    "total_cache_read_tokens": 0,
                    "total_output_tokens": 0,
                    "estimated_usd_saved": 0.0
                }
            },
            "slices": [{"id": "ABC-001", "status": "Planned"}]
        }
        self.writer.write(data)
        self.assertTrue(self.output_path.exists())
        with open(self.output_path, 'r') as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data["metadata"]["total_slices"], 1)

if __name__ == '__main__':
    unittest.main()
