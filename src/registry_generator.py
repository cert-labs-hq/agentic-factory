#!/usr/bin/env python3
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class RegistryGenerator:
    def __init__(self):
        self.root = Path(__file__).resolve().parent.parent if Path(__file__).resolve().parent.name == "src" else Path(__file__).resolve().parent
        self.slices_dir = self.root / ".factory" / "slices"
        self.output_path = self.root / ".factory" / "index.json"
        self.telemetry_path = self.root / ".factory" / "telemetry.json"
        self.slice_pattern = re.compile(r"^[a-zA-Z]{2,4}-?[0-9]{3,}.*\.json$", re.IGNORECASE)

    def get_telemetry_data(self):
        """Aggregates totals and per-slice usage from logs."""
        data = {
            "global": {"prompt": 0, "reasoning": 0, "output": 0, "total": 0},
            "phases": {},
            "slices": defaultdict(lambda: {"prompt": 0, "reasoning": 0, "output": 0, "total": 0})
        }
        
        if not self.telemetry_path.exists(): return data

        with open(self.telemetry_path, 'r') as f:
            t_data = json.load(f)
            logs = t_data.get("logs", [])
            
            # Use the explicit global total if provided
            data["global"] = t_data.get("project_total_cost", data["global"])

            for log in logs:
                sid = log.get("slice_id")
                phase = log.get("phase", "unknown").lower()
                tokens = log.get("tokens", {})
                
                # 1. Per-Phase Aggregation
                if phase not in data["phases"]:
                    data["phases"][phase] = {"prompt": 0, "reasoning": 0, "output": 0, "total": 0}
                
                # 2. Per-Slice Aggregation
                for k in ["prompt", "reasoning", "output", "total"]:
                    val = tokens.get(k, 0)
                    data["phases"][phase][k] += val
                    if sid:
                        data["slices"][sid][k] += val

        return data

    def aggregate(self):
        tele = self.get_telemetry_data()
        final_slices = []

        if self.slices_dir.exists():
            for p in self.slices_dir.glob("*.json"):
                if p.name == "index.json" or not self.slice_pattern.match(p.name):
                    continue
                try:
                    with open(p, 'r') as f:
                        s_data = json.load(f)
                        sid = s_data.get("id")
                        
                        # SYNC LOGIC: Overwrite file data with actual Telemetry sums
                        if sid in tele["slices"]:
                            s_data["token_usage"] = tele["slices"][sid]
                        
                        final_slices.append(s_data)
                except: continue

        index = {
            "metadata": {
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "total_slices": len(final_slices),
                "global_finops": {
                    "total_combined_tokens": tele["global"]["total"],
                    "project_total_cost": tele["global"],
                    "phase_stats": tele["phases"]
                }
            },
            "slices": final_slices
        }

        with open(self.output_path, 'w') as f:
            json.dump(index, f, indent=2)
        print(f"✅ Sync Complete: {len(final_slices)} slices synced with Telemetry.")

if __name__ == "__main__":
    RegistryGenerator().aggregate()