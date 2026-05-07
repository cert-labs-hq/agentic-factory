import json
import argparse
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

class SliceValidator:
    """
    Validates individual slice JSON files against the master schema contract.
    Uses standard library only to minimize dependencies.
    """
    def __init__(self, schema_path: Path):
        """
        Initializes the validator with the path to the master schema.
        
        :param schema_path: Path to .factory/contracts/schema_file.json
        """
        self.schema_path = schema_path
        with open(self.schema_path, 'r') as f:
            self.schema = json.load(f)
        self.required_fields = self.schema.get("required", [])

    def validate(self, slice_data: Dict[str, Any]) -> bool:
        """
        Validates the provided slice data against the schema's required fields.
        
        :param slice_data: Dictionary containing slice metadata.
        :return: True if valid, False otherwise.
        """
        # Check for required fields at the root
        for field in self.required_fields:
            if field not in slice_data:
                return False
        
        # Additional checks can be added here for types/enums if necessary
        # For MVP, checking existence of required fields is sufficient
        return True

class RegistryAggregator:
    """
    Scans the slices directory and aggregates metadata into a unified registry structure.
    """
    def __init__(self, slices_dir: Path, validator: SliceValidator):
        """
        Initializes the aggregator with the source directory and a validator.
        """
        self.slices_dir = slices_dir
        self.validator = validator
        self.slice_pattern = re.compile(r"^[A-Z]{3}-[0-9]{3}.*\.json$")

    def discover_slices(self) -> List[Path]:
        """
        Scans the slices directory for valid JSON files matching the [A-Z]{3}-[0-9]{3} pattern.
        """
        if not self.slices_dir.exists():
            return []
        return [p for p in self.slices_dir.glob("*.json") if self.slice_pattern.match(p.name)]

    def aggregate(self) -> Dict[str, Any]:
        """
        Reads discovered slices, validates them, and produces the aggregated registry object.
        """
        discovered = self.discover_slices()
        slices_data = []
        status_counts = {
            "Proposed": 0, "Planned": 0, "Quota-Blocked": 0, "In Progress": 0, 
            "In Review": 0, "Approved": 0, "Warehoused": 0, "Rejected": 0
        }
        total_tokens = 0

        for slice_path in discovered:
            with open(slice_path, 'r') as f:
                try:
                    data = json.load(f)
                    if self.validator.validate(data):
                        slices_data.append(data)
                        status = data.get("status")
                        if status in status_counts:
                            status_counts[status] += 1
                        
                        # Sum tokens from forecast or usage if available
                        forecast = data.get("forecast", {})
                        est_tokens = forecast.get("estimated_tokens", {})
                        total_tokens += est_tokens.get("prompt", 0) + est_tokens.get("reasoning", 0) + est_tokens.get("output", 0)
                except json.JSONDecodeError:
                    continue

        registry = {
            "metadata": {
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "total_slices": len(slices_data),
                "status_summary": status_counts,
                "global_finops": {
                    "total_combined_tokens": total_tokens,
                    # Placeholders for other FinOps metrics
                    "total_prompt_tokens": 0,
                    "total_reasoning_tokens": 0,
                    "total_cache_read_tokens": 0,
                    "total_output_tokens": 0,
                    "estimated_usd_saved": 0.0
                }
            },
            "slices": slices_data
        }
        return registry

class RegistryWriter:
    """
    Handles the serialization and validation of the final index.json registry file.
    """
    def __init__(self, output_path: Path, aggregate_schema_path: Path):
        """
        Initializes the writer with the destination and the aggregate contract path.
        """
        self.output_path = output_path
        self.aggregate_schema_path = aggregate_schema_path
        with open(self.aggregate_schema_path, 'r') as f:
            self.schema = json.load(f)
        self.required_root = self.schema.get("required", [])

    def validate_aggregate(self, registry_data: Dict[str, Any]) -> bool:
        """
        Basic validation of the aggregate registry data.
        """
        for field in self.required_root:
            if field not in registry_data:
                return False
        return True

    def write(self, registry_data: Dict[str, Any]) -> None:
        """
        Serializes the registry data to JSON and writes it to the output path.
        """
        if not self.validate_aggregate(registry_data):
            raise ValueError("Registry data violates aggregate schema")

        with open(self.output_path, 'w') as f:
            json.dump(registry_data, f, indent=2)
        print(f"Registry written successfully to {self.output_path}")

def main():
    parser = argparse.ArgumentParser(description="Deterministic Registry Aggregator")
    parser.add_argument("--slices-dir", type=str, default=".factory/slices", help="Directory containing slice JSONs")
    parser.add_argument("--output", type=str, default=".factory/index.json", help="Path to output registry file")
    parser.add_argument("--schema", type=str, default=".factory/contracts/schema_file.json", help="Master slice schema")
    parser.add_argument("--aggregate-schema", type=str, default=".factory/contracts/aggregate_slice_info.json", help="Aggregate registry schema")
    
    args = parser.parse_args()
    
    slices_dir = Path(args.slices_dir)
    output_path = Path(args.output)
    schema_path = Path(args.schema)
    agg_schema_path = Path(args.aggregate_schema)

    try:
        print(f"--- Starting Registry Generation ---")
        validator = SliceValidator(schema_path)
        aggregator = RegistryAggregator(slices_dir, validator)
        writer = RegistryWriter(output_path, agg_schema_path)

        registry_data = aggregator.aggregate()
        writer.write(registry_data)
        
        print(f"Success: Aggregated {registry_data['metadata']['total_slices']} slices into {output_path}")
        print(f"--- Registry Generation Complete ---")
    except Exception as e:
        print(f"Error during registry generation: {e}")
        exit(1)

if __name__ == "__main__":
    main()
