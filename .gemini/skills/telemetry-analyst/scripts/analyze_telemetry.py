import json
import os

TELEMETRY_PATH = '.factory/telemetry.json'
SUMMARY_PATH = '.factory/telemetry_summary.json'

def analyze():
    if not os.path.exists(TELEMETRY_PATH):
        print(f"Error: {TELEMETRY_PATH} not found.")
        return

    with open(TELEMETRY_PATH, 'r') as f:
        data = json.load(f)

    logs = data.get('logs', [])
    summary = {
        "total_cost": data.get('project_total_cost', {}),
        "phases": {}
    }

    for log in logs:
        phase = log.get('phase', 'unknown')
        tokens = log.get('tokens', {})
        
        if phase not in summary['phases']:
            summary['phases'][phase] = {
                "input_tokens": 0,
                "reasoning_tokens": 0,
                "output_tokens": 0,
                "count": 0
            }
        
        p = summary['phases'][phase]
        p['input_tokens'] += tokens.get('input', 0)
        p['reasoning_tokens'] += tokens.get('reasoning', 0)
        p['output_tokens'] += tokens.get('output', 0)
        p['count'] += 1

    with open(SUMMARY_PATH, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Summary updated successfully in {SUMMARY_PATH}")

if __name__ == "__main__":
    analyze()
