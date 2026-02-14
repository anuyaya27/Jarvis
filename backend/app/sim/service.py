import json
from typing import Any

from app.kb.service import KBService
from app.providers.interfaces import LLMProvider
from app.schemas import SimulateRequest, SimulationResult
from app.sim.prompt_builder import PromptBuilder


class SimulationService:
    def __init__(self, llm_provider: LLMProvider, kb_service: KBService):
        self._llm = llm_provider
        self._kb = kb_service
        self._prompts = PromptBuilder()

    def run(self, req: SimulateRequest) -> SimulationResult:
        decision_text = req.decision_text or req.transcript or ""
        retrieved = self._kb.context_for_docs(req.context_doc_ids)
        prompt = self._prompts.build(decision_text, retrieved, req.constraints)
        result = self._llm.simulate_decision(prompt, retrieved, req.constraints)
        result.branches = limit_branches(result.branches)
        return result

    def extract_decision_spec(self, transcript: str) -> dict[str, Any]:
        prompt = (
            "Extract a compact decision spec in JSON with keys: objective, timeframe, macro_conditions.\n"
            f"Transcript: {transcript}"
        )
        raw = self._llm.generate_json(prompt)
        try:
            return json.loads(raw.content)
        except Exception:
            return {"objective": transcript, "timeframe": "unspecified", "macro_conditions": []}


def limit_branches(branches: list, max_branches: int = 6) -> list:
    return branches[:max_branches]
