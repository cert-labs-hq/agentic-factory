#!/usr/bin/env python3
import json
import argparse
import re
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

class SliceValidator:
    """
    Validates individual slice JSON files against the master schema contract.
    """
    def __init__(self, schema_path: Path):
        """
        Initializes the validator with the path to the master schema.
        """
        if not schema_path.exists():
            # Fallback/Safety: If schema is missing, use minimal required fields
            self.required_fields = ["id", "title", "status"]
        else:
            with open(schema_path, 'r') as f:
                schema = json.load(f)
            self.required_fields = schema.get("required", [])

    def validate(self, slice_data: Dict[str, Any]) -> bool:
        """
        Validates the provided slice data against the schema's required fields.
        """
        for field in self.required_fields:
            if field not in slice_data:
                return False
        return True

class RegistryAggregator:
    """
    Scans the slices directory and aggregates metadata into a unified registry structure.
    """
    def __init__(self, slices_dir: Path, validator: SliceValidator, telemetry_path: Path = Path(".factory/telemetry.json")):
        self.slices_dir = slices_dir
        self.validator = validator
        self.telemetry_path = telemetry_path
        # Pattern to match slice JSON files like BKP-001-name.json
        self.slice_pattern = re.compile(r"^[A-Z]{3}-[0-9]{3}.*\.json$")

    def discover_slices(self) -> List[Path]:
        if not self.slices_dir.exists():
            self.slices_dir.mkdir(parents=True, exist_ok=True)
            return []
        # Filter files that match the pattern and are NOT the index.json itself
        return [p for p in self.slices_dir.glob("*.json") 
                if self.slice_pattern.match(p.name) and p.name != "index.json"]

    def aggregate_telemetry(self) -> Dict[str, Any]:
        """
        Aggregates FinOps metrics from telemetry.json.
        """
        if not self.telemetry_path.exists():
            return {
                "project_total_cost": {"prompt": 0, "reasoning": 0, "output": 0, "total": 0},
                "phase_stats": {}
            }
        
        with open(self.telemetry_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return {
                    "project_total_cost": {"prompt": 0, "reasoning": 0, "output": 0, "total": 0},
                    "phase_stats": {}
                }
            
        logs = data.get("logs", [])
        # Extract total cost if available, otherwise default
        project_total = data.get("project_total_cost", {"prompt": 0, "reasoning": 0, "output": 0, "total": 0})
        
        phase_stats = {}
        for log in logs:
            phase = log.get("phase", "unknown")
            tokens = log.get("tokens", {})
            
            if phase not in phase_stats:
                phase_stats[phase] = {"prompt": 0, "reasoning": 0, "output": 0, "total": 0}
            
            phase_stats[phase]["prompt"] += tokens.get("prompt", 0)
            phase_stats[phase]["reasoning"] += tokens.get("reasoning", 0)
            phase_stats[phase]["output"] += tokens.get("output", 0)
            phase_stats[phase]["total"] += tokens.get("total", 0)
            
        return {
            "project_total_cost": project_total,
            "phase_stats": phase_stats
        }

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
        
        # Telemetry aggregation
        telemetry_metrics = self.aggregate_telemetry()

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
                    "estimated_usd_saved": round(usd_saved, 6),
                    "project_total_cost": telemetry_metrics["project_total_cost"],
                    "phase_stats": telemetry_metrics["phase_stats"]
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
    # Updated default output path to be inside the slices folder
    parser.add_argument("--output", default=".factory/slices/index.json", help="Output JSON path")
    parser.add_argument("--schema", default=".factory/contracts/aggregate_slice_info.json", help="Input schema")
    parser.add_argument("--telemetry", default=".factory/telemetry.json", help="Source telemetry file")
    
    args = parser.parse_args()
    
    try:
        print("--- Starting Registry Generation ---")
        validator = SliceValidator(Path(args.schema))
        aggregator = RegistryAggregator(Path(args.slices), validator, Path(args.telemetry))
        writer = RegistryWriter(Path(args.output))

        registry_data = aggregator.aggregate()
        writer.write(registry_data)
        
        print(f"📊 Stats: {registry_data['metadata']['total_slices']} slices | ${registry_data['metadata']['global_finops']['estimated_usd_saved']} saved.")
        print(f"💰 Global Investment: {registry_data['metadata']['global_finops']['project_total_cost']['total']} tokens.")
        print("--- Registry Generation Complete ---")
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()
