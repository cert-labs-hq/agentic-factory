import json
import os
from datetime import datetime, timedelta, timezone

TELEMETRY_PATH = '.factory/telemetry.json'
SUMMARY_PATH = '.factory/telemetry_summary.json'
DAILY_LIMIT = 500000

def analyze():
    if not os.path.exists(TELEMETRY_PATH):
        print(f"Error: {TELEMETRY_PATH} not found.")
        return

    with open(TELEMETRY_PATH, 'r') as f:
        data = json.load(f)

    logs = data.get('logs', [])
    project_total = data.get('project_total_cost', {})
    
    # Precise Temporal Tracking
    now = datetime.now(timezone.utc)
    cutoff_24h = now - timedelta(hours=24)
    
    # Reset is at Midnight UTC
    next_reset = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    time_to_reset = next_reset - now
    hours_to_reset = int(time_to_reset.total_seconds() // 3600)
    minutes_to_reset = int((time_to_reset.total_seconds() % 3600) // 60)
    
    used_24h = 0

    summary = {
        "total_cost": {
            "prompt_tokens": project_total.get('prompt', 0),
            "reasoning_tokens": project_total.get('reasoning', 0),
            "output_tokens": project_total.get('output', 0),
            "total_tokens": project_total.get('total', 0)
        },
        "phases": {},
        "slices": {}
    }

    for log in logs:
        try:
            log_time = datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00'))
        except ValueError:
            continue
            
        tokens = log.get('tokens', {})
        total_tokens = tokens.get('total', 0)

        # Sum for 24h window based on REAL time
        if log_time > cutoff_24h:
            used_24h += total_tokens

        phase = log.get('phase', 'unknown')
        slice_id = log.get('slice_id', 'unknown')
        
        # Aggregate by Phase
        if phase not in summary['phases']:
            summary['phases'][phase] = {
                "prompt_tokens": 0, "reasoning_tokens": 0, "output_tokens": 0, "total_tokens": 0, "count": 0
            }
        p = summary['phases'][phase]
        p['prompt_tokens'] += tokens.get('prompt', 0)
        p['reasoning_tokens'] += tokens.get('reasoning', 0)
        p['output_tokens'] += tokens.get('output', 0)
        p['total_tokens'] += total_tokens
        p['count'] += 1

        # Aggregate by Slice
        if slice_id not in summary['slices']:
            summary['slices'][slice_id] = {
                "prompt_tokens": 0, "reasoning_tokens": 0, "output_tokens": 0, "total_tokens": 0, "count": 0
            }
        s = summary['slices'][slice_id]
        s['prompt_tokens'] += tokens.get('prompt', 0)
        s['reasoning_tokens'] += tokens.get('reasoning', 0)
        s['output_tokens'] += tokens.get('output', 0)
        s['total_tokens'] += total_tokens
        s['count'] += 1

    # Final Quota Calculation
    used_percentage = (used_24h / DAILY_LIMIT) * 100
    remaining = DAILY_LIMIT - used_24h
    remaining_percentage = (remaining / DAILY_LIMIT) * 100
    
    quota = {
        "daily_limit": DAILY_LIMIT,
        "used_24h": used_24h,
        "used_percentage": f"{used_percentage:.1f}%",
        "remaining": max(0, remaining),
        "remaining_percentage": f"{max(0, remaining_percentage):.1f}%",
        "hours_to_reset": f"{hours_to_reset}h {minutes_to_reset}m",
        "last_updated_at": now.isoformat(),
        "next_reset_at": next_reset.isoformat()
    }

    data['quota_governance'] = quota
    summary['quota_governance'] = quota

    with open(TELEMETRY_PATH, 'w') as f:
        json.dump(data, f, indent=2)

    with open(SUMMARY_PATH, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Update Successful. Quota Used: {used_percentage:.1f}%. Reset in {hours_to_reset}h.")

if __name__ == "__main__":
    analyze()
