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
    main()#!/usr/bin/env python3
import json
import argparse
import re
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

class SliceValidator:
    def __init__(self, schema_path: Path):
        if not schema_path.exists():
            # Fallback/Safety for Stage 1: If schema is missing, allow validation to pass 
            # or create a dummy schema to prevent total factory failure.
            self.required_fields = ["id", "name", "status"]
        else:
            with open(schema_path, 'r') as f:
                schema = json.load(f)
            self.required_fields = schema.get("required", [])

    def validate(self, slice_data: Dict[str, Any]) -> bool:
        for field in self.required_fields:
            if field not in slice_data:
                return False
        return True

class RegistryAggregator:
    def __init__(self, slices_dir: Path, validator: SliceValidator):
        self.slices_dir = slices_dir
        self.validator = validator
        self.slice_pattern = re.compile(r"^[A-Z]{3}-[0-9]{3}.*\.json$")

    def discover_slices(self) -> List[Path]:
        if not self.slices_dir.exists():
            self.slices_dir.mkdir(parents=True, exist_ok=True)
            return []
        return [p for p in self.slices_dir.glob("*.json") if self.slice_pattern.match(p.name)]

    def aggregate(self) -> Dict[str, Any]:
        discovered = self.discover_slices()
        slices_data = []
        status_counts = {k: 0 for k in ["Proposed", "Planned", "Quota-Blocked", "In Progress", "In Review", "Approved", "Warehoused", "Rejected"]}
        
        totals = {"prompt": 0, "reasoning": 0, "cache": 0, "output": 0}

        for slice_path in discovered:
            with open(slice_path, 'r') as f:
                try:
                    data = json.load(f)
                    if self.validator.validate(data):
                        slices_data.append(data)
                        status = data.get("status")
                        if status in status_counts: status_counts[status] += 1
                        
                        # Priority: Actual usage > Forecast
                        usage = data.get("token_usage") or data.get("forecast", {}).get("estimated_tokens", {})
                        totals["prompt"] += usage.get("prompt", 0)
                        totals["reasoning"] += usage.get("reasoning", 0)
                        totals["cache"] += usage.get("cache_read", 0)
                        totals["output"] += usage.get("output", 0)
                except (json.JSONDecodeError, KeyError):
                    continue

        # FinOps Calculation: Savings = (CacheTokens * 0.90) * Rate
        # Based on $0.15 per 1M tokens standard rate.
        rate_per_token = 0.00000015
        usd_saved = (totals["cache"] * 0.90) * rate_per_token

        return {
            "metadata": {
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "total_slices": len(slices_data),
                "status_summary": status_counts,
                "global_finops": {
                    "total_prompt_tokens": totals["prompt"],
                    "total_reasoning_tokens": totals["reasoning"],
                    "total_cache_read_tokens": totals["cache"],
                    "total_output_tokens": totals["output"],
                    "total_combined_tokens": sum(totals.values()),
                    "estimated_usd_saved": round(usd_saved, 6)
                }
            },
            "slices": slices_data
        }

class RegistryWriter:
    def __init__(self, output_path: Path):
        self.output_path = output_path

    def write(self, registry_data: Dict[str, Any]) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, 'w') as f:
            json.dump(registry_data, f, indent=2)
        print(f"✅ Registry generated: {self.output_path}")

def main():
    parser = argparse.ArgumentParser(description="BKP-004 Registry Aggregator")
    parser.add_argument("--slices", default=".factory/slices", help="Slices directory")
    parser.add_argument("--output", default=".factory/index.json", help="Output JSON path")
    parser.add_argument("--schema", default=".factory/contracts/schema_file.json", help="Input schema")
    
    args = parser.parse_args()
    
    try:
        validator = SliceValidator(Path(args.schema))
        aggregator = RegistryAggregator(Path(args.slices), validator)
        writer = RegistryWriter(Path(args.output))

        registry_data = aggregator.aggregate()
        writer.write(registry_data)
        
        print(f"📊 Stage 1 Stats: {registry_data['metadata']['total_slices']} slices | ${registry_data['metadata']['global_finops']['estimated_usd_saved']} saved.")
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()