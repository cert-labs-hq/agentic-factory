import os
import time
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource 
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Safely extract environment keys from your repo root configuration
load_dotenv()

class AgenticHarness:
    def __init__(self):
        # 1. Initialize OpenTelemetry Pipeline targeting the Local Collector
        resource = Resource.create(attributes={
            "service.name": "gemini-harness-lab",
            "environment": "research-dev"
        })
        
        provider = TracerProvider(resource=resource)
        processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True))
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        
        self.tracer = trace.get_tracer("sdd.core")
        
        # 2. Configure Modern Gemini Client
        self.client = genai.Client()
        self.model_name = "gemini-2.5-flash"
        
        # 3. Establish Local Telemetry Pathing (The "Skills" Registry System)
        self.root = Path(__file__).resolve().parent.parent
        self.telemetry_path = self.root / ".factory" / "telemetry.json"

    def _write_local_telemetry(self, slice_id: str, phase: str, prompt_tk: int, reasoning_tk: int, output_tk: int):
        """
        Maintains structural continuity with registry_generator.py by performing a concurrent
        local write operation into the .factory workspace.
        """
        self.telemetry_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize or load historical local data contract
        if self.telemetry_path.exists():
            try:
                with open(self.telemetry_path, "r") as f:
                    local_data = json.load(f)
            except Exception:
                local_data = {"logs": []}
        else:
            local_data = {"logs": []}
            
        if "logs" not in local_data:
            local_data["logs"] = []
            
        # Append structured block precisely matching aggregate_telemetry tracking patterns
        local_data["logs"].append({
            "slice_id": slice_id,
            "phase": phase.lower(),
            "tokens": {
                "prompt": prompt_tk,
                "reasoning": reasoning_tk,
                "output": output_tk,
                "total": prompt_tk + reasoning_tk + output_tk
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
        
        with open(self.telemetry_path, "w") as f:
            json.dump(local_data, f, indent=2)

    def execute_sdd_step(self, slice_id: str, phase: str, prompt: str):
        """
        Executes a Spec-Driven Development prompt, wrapping inference inside 
        nested OTel Spans and broadcasting data to both OpenObserve and local JSON registries.
        """
        with self.tracer.start_as_current_span("sdd.lifecycle_span") as parent_span:
            parent_span.set_attribute("sdd.slice_id", slice_id)
            parent_span.set_attribute("sdd.phase", phase.lower())
            
            start_time_nano = int(time.time() * 1e9)
            
            # Execute model invocation with explicit thinking config parameters enabled
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(
                        thinking_budget=2048  # Forces model to allocate structural reasoning tokens
                    )
                )
            )
            
            end_time_nano = int(time.time() * 1e9)
            usage = response.usage_metadata
            
            # FIXED: Target the exact SDK metadata property 'thoughts_token_count'
            prompt_tokens = getattr(usage, "prompt_token_count", 0) or 0
            candidate_tokens = getattr(usage, "candidates_token_count", 0) or 0
            reasoning_tokens = getattr(usage, "thoughts_token_count", 0) or 0 
            completion_tokens = max(0, candidate_tokens - reasoning_tokens)

            # 1. Broadcast to the Distributed Observability Plane (OpenObserve)
            child_span = self.tracer.start_span(
                name="ai.reasoning_span",
                start_time=start_time_nano
            )
            try:
                child_span.set_attribute("sdd.phase", phase.lower())
                child_span.set_attribute("gen_ai.usage.prompt_tokens", prompt_tokens)
                child_span.set_attribute("gen_ai.usage.reasoning_tokens", reasoning_tokens)
                child_span.set_attribute("gen_ai.usage.completion_tokens", completion_tokens)
                
                cost = (prompt_tokens * 0.000000075) + (reasoning_tokens * 0.00000030)
                child_span.set_attribute("industrial.cost.reasoning", round(cost, 7))
            finally:
                child_span.end(end_time=end_time_nano)

            # 2. Broadcast to the Local File-Based Observability Layer (Skills Registry)
            self._write_local_telemetry(slice_id, phase, prompt_tokens, reasoning_tokens, completion_tokens)

            return response.text

if __name__ == "__main__":
    harness = AgenticHarness()
    
    test_runner_prompt = """
    Context: Slice BKP-004 successfully implemented the unit and integration tests located in the /tests folder.
    
    Task: Write a deterministic bash run script (run_tests.sh) that executes these specific tests.
    Requirements:
    1. Check for the virtual environment (.venv) and activate it if present.
    2. Execute the tests using pytest, outputting a verbose log.
    3. Include clean exit codes to integrate cleanly into an upstream IDP/CI pipeline.
    4. Provide ONLY the raw bash code within a single markdown block.
    """
    
    print("🚀 Dispatched task for BKP-004 Run Script...")
    output = harness.execute_sdd_step(
        slice_id="BKP-004", 
        phase="Validation", 
        prompt=test_runner_prompt
    )
    
    print("\n✅ Inference Complete! Output Generated:")
    print("-" * 50)
    print(output)
    print("-" * 50)
    print("Telemetry dual-write successful. Data sent to OpenObserve and local index.")