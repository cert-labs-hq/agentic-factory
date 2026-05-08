#!/usr/bin/env python3
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class RegistryGenerator:
    def __init__(self):
        # Path resolution
        self.root = Path(__file__).resolve().parent.parent if Path(__file__).resolve().parent.name == "src" else Path(__file__).resolve().parent
        self.slices_dir = self.root / ".factory" / "slices"
        self.output_path = self.root / ".factory" / "index.json"
        self.telemetry_path = self.root / ".factory" / "telemetry.json"
        self.slice_pattern = re.compile(r"^[a-zA-Z]{2,4}-?[0-9]{3,}.*\.json$", re.IGNORECASE)

    def aggregate_telemetry(self):
        """
        Calculates project totals and phase stats from logs.
        Ignores the stale 'project_total_cost' header in telemetry.json to ensure congruence.
        """
        # We start at zero and build the truth from the logs
        metrics = {
            "global": {"prompt": 0, "reasoning": 0, "output": 0, "total": 0},
            "phases": {},
            "slices": defaultdict(lambda: {"prompt": 0, "reasoning": 0, "output": 0, "total": 0})
        }
        
        if not self.telemetry_path.exists(): return metrics

        with open(self.telemetry_path, 'r') as f:
            t_data = json.load(f)
            logs = t_data.get("logs", [])

            for log in logs:
                sid = log.get("slice_id")
                phase = log.get("phase", "unknown").lower()
                tokens = log.get("tokens", {})
                
                # Update Global, Phase, and Slice accumulators
                for k in ["prompt", "reasoning", "output", "total"]:
                    val = tokens.get(k, 0)
                    
                    # 1. Global (The Source of Truth)
                    metrics["global"][k] += val
                    
                    # 2. Phase Breakdown
                    if phase not in metrics["phases"]:
                        metrics["phases"][phase] = {"prompt": 0, "reasoning": 0, "output": 0, "total": 0}
                    metrics["phases"][phase][k] += val
                    
                    # 3. Individual Slice Usage
                    if sid:
                        metrics["slices"][sid][k] += val

        return metrics

    def aggregate(self):
        tele = self.aggregate_telemetry()
        final_slices = []

        if self.slices_dir.exists():
            for p in self.slices_dir.glob("*.json"):
                if p.name == "index.json" or not self.slice_pattern.match(p.name):
                    continue
                try:
                    with open(p, 'r') as f:
                        s_data = json.load(f)
                        sid = s_data.get("id")
                        # Sync slice object with actual telemetry usage
                        if sid in tele["slices"]:
                            s_data["token_usage"] = tele["slices"][sid]
                        final_slices.append(s_data)
                except: continue

        # Final Congruent Assembly
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
            
        print(f"✅ Congruence Sync: Project Total ({tele['global']['total']}) matches sum of all phases.")

if __name__ == "__main__":
    RegistryGenerator().aggregate()