# Generate valid real-time nanosecond timestamps for your Ubuntu environment
START_TIME=$(date +%s)000000000
END_TIME=$(($(date +%s) + 2))000000000

curl -X POST http://localhost:4318/v1/traces \
  -H "Content-Type: application/json" \
  -d '{
    "resourceSpans": [
      {
        "resource": {
          "attributes": [
            { "key": "service.name", "value": { "stringValue": "gemini-harness-lab" } },
            { "key": "environment", "value": { "stringValue": "research-dev" } }
          ]
        },
        "scopeSpans": [
          {
            "scope": { "name": "sdd.core" },
            "spans": [
              {
                "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
                "spanId": "00f067aa0ba902b7",
                "name": "ai.reasoning_span",
                "kind": 3,
                "startTimeUnixNano": "'"$START_TIME"'",
                "endTimeUnixNano": "'"$END_TIME"'",
                "attributes": [
                  { "key": "sdd.phase", "value": { "stringValue": "planning" } },
                  { "key": "gen_ai.usage.reasoning_tokens", "value": { "intValue": 1420 } },
                  { "key": "gen_ai.usage.prompt_tokens", "value": { "intValue": 2800 } },
                  { "key": "industrial.cost.reasoning", "value": { "doubleValue": 0.00994 } }
                ],
                "status": { "code": 1 }
              }
            ]
          }
        ]
      }
    ]
  }'