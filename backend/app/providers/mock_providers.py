import hashlib
import json
import math
import time
import uuid
from typing import Any

from app.providers.interfaces import (
    AgentAutomationProvider,
    EmbeddingProvider,
    LLMProvider,
    LLMResponse,
    SpeechProvider,
)
from app.schemas import AuditMeta, Branch, FailureTrigger, KPISet, Mitigation, RiskCluster, SimulationResult, StressPoint


class MockLLMProvider(LLMProvider):
    def simulate_decision(self, prompt: str, context: list[str], constraints: dict[str, Any]) -> SimulationResult:
        _ = prompt, context, constraints
        return SimulationResult(
            decision_id=str(uuid.uuid4()),
            input_summary="Simulate acquiring Competitor X under recession next quarter.",
            assumptions=[
                "Credit markets tighten by 20%",
                "Competitor X valuation drops 12%",
                "Integration costs peak in Q2",
            ],
            branches=[
                Branch(
                    branch_name="optimistic",
                    narrative="Fast integration unlocks cross-sell gains.",
                    key_events=["Deal closes in 45 days", "Key talent retained", "Synergies realized by Q3"],
                    KPIs=KPISet(revenue=182.5, margin=19.2, burn=8.5, headcount=1240, churn=2.8),
                    risk_clusters=[RiskCluster(tag="integration", severity="medium")],
                    stress_points=[StressPoint(resource="cash", threshold="burn > 12m/month")],
                    failure_triggers=[FailureTrigger(condition="Retention < 85%", impact="synergy delay 2 quarters")],
                    mitigations=[Mitigation(rank=1, action="Retention bonuses for top 10% talent")],
                    stability_score=82,
                ),
                Branch(
                    branch_name="base",
                    narrative="Moderate slowdown with manageable integration drag.",
                    key_events=["Deal closes in 60 days", "Two systems migrated", "Gross margin flat"],
                    KPIs=KPISet(revenue=160.2, margin=15.4, burn=11.1, headcount=1190, churn=4.2),
                    risk_clusters=[RiskCluster(tag="financing", severity="high")],
                    stress_points=[StressPoint(resource="debt covenant", threshold="net leverage > 3.5x")],
                    failure_triggers=[FailureTrigger(condition="Revenue miss > 10%", impact="refinancing risk")],
                    mitigations=[Mitigation(rank=1, action="Stage payments tied to post-close KPI gates")],
                    stability_score=63,
                ),
                Branch(
                    branch_name="pessimistic",
                    narrative="Recession deepens and integration stalls.",
                    key_events=["Credit spreads widen", "Customer churn spikes", "Operational overlap persists"],
                    KPIs=KPISet(revenue=133.9, margin=10.1, burn=15.7, headcount=1140, churn=8.9),
                    risk_clusters=[RiskCluster(tag="liquidity", severity="critical")],
                    stress_points=[StressPoint(resource="cash runway", threshold="< 8 months")],
                    failure_triggers=[FailureTrigger(condition="Runway < 6 months", impact="forced divestiture")],
                    mitigations=[Mitigation(rank=1, action="Pre-negotiate bridge facility before close")],
                    stability_score=38,
                ),
            ],
            overall_recommendation="Proceed only with staged close terms and pre-funded liquidity buffer.",
            audit=AuditMeta(model_id="mock.nova-lite", latency_ms=24, tokens_input=600, tokens_output=420),
        )

    def generate_json(self, prompt: str) -> LLMResponse:
        if "decision_title" in prompt and "time_horizon" in prompt:
            payload = {
                "decision_title": "Acquire Competitor X",
                "objective": "Evaluate acquisition under recession conditions",
                "options": ["acquire", "strategic partnership", "defer"],
                "constraints": ["cash runway", "regulatory complexity"],
                "time_horizon": "next quarter",
                "market_context": "recessionary demand pressure",
                "key_assumptions": ["financing available", "integration team capacity"],
            }
            return LLMResponse(content=json.dumps(payload), model_id="mock.nova-lite", latency_ms=10, tokens_input=40, tokens_output=30)
        # Deterministic payload based on prompt hash for testability.
        h = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:12]
        payload = {"prompt_hash": h, "status": "ok"}
        return LLMResponse(content=json.dumps(payload), model_id="mock.nova-lite", latency_ms=10, tokens_input=10, tokens_output=8)


class MockSpeechProvider(SpeechProvider):
    def create_session(self) -> str:
        return str(uuid.uuid4())

    def process_audio_chunk(self, session_id: str, audio_chunk: bytes) -> dict[str, Any]:
        transcript = f"[{session_id[:8]}] partial transcript, bytes={len(audio_chunk)}"
        return {
            "partial_transcript": transcript,
            "final_transcript": "Simulate acquiring Competitor X under recession next quarter.",
            "audio_base64": "",
        }


class MockEmbeddingProvider(EmbeddingProvider):
    dim: int = 32

    def _embed(self, text: str) -> list[float]:
        h = hashlib.sha256(text.encode("utf-8")).digest()
        vals = [h[i] / 255.0 for i in range(self.dim)]
        norm = math.sqrt(sum(v * v for v in vals)) or 1.0
        return [v / norm for v in vals]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)


class MockNovaActProvider(AgentAutomationProvider):
    def run_playbook(self, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        time.sleep(0.02)
        return {
            "playbook": name,
            "status": "stubbed",
            "summary": "Nova Act stub executed. TODO: wire real browser workflow automation.",
            "input": payload,
        }
