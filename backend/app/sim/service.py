import json
from typing import Any

from app.kb.service import KBService
from app.providers.interfaces import LLMProvider
from app.schemas import DecisionSpec, SimulateRequest, SimulationResult
from app.sim.prompt_builder import PromptBuilder


class SimulationService:
    def __init__(self, llm_provider: LLMProvider, kb_service: KBService):
        self._llm = llm_provider
        self._kb = kb_service
        self._prompts = PromptBuilder()

    def run(self, req: SimulateRequest) -> SimulationResult:
        decision_text = req.decision_text or req.transcript or ""
        decision_spec = self.extract_decision_spec(decision_text)
        retrieved = self._kb.context_for_docs(req.context_doc_ids)
        prompt = self._prompts.build(decision_text, retrieved, req.constraints, decision_spec=decision_spec)
        result = self._llm.simulate_decision(prompt, retrieved, req.constraints)
        result.branches = limit_branches(result.branches)
        return result

    def extract_decision_spec(self, transcript: str) -> DecisionSpec:
        prompt = self._prompts.build_decision_spec(transcript)
        raw = self._llm.generate_json(prompt)
        try:
            parsed = json.loads(raw.content)
            return DecisionSpec.model_validate(parsed)
        except Exception:
            return self._deterministic_decision_spec(transcript)

    def _deterministic_decision_spec(self, transcript: str) -> DecisionSpec:
        text = " ".join(transcript.split())
        horizon = "next quarter" if "quarter" in text.lower() else "12 months"
        return DecisionSpec(
            decision_title=(text[:80] + "...") if len(text) > 80 else text,
            objective=text,
            options=["proceed", "delay", "decline"],
            constraints=["capital efficiency", "execution risk"],
            time_horizon=horizon,
            market_context="uncertain macro conditions",
            key_assumptions=["market demand remains volatile", "financing remains available"],
        )


def limit_branches(branches: list, max_branches: int = 6) -> list:
    return branches[:max_branches]
