import json
from typing import Any

from app.kb.service import KBService
from app.providers.interfaces import LLMProvider
from app.schemas import DecisionSpec, SimulateRequest, SimulationResult
from app.sim.prompt_builder import PromptBuilder
from app.sim.scoring import compute_stability_score


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
        for branch in result.branches:
            llm_score = branch.llm_stability_score if branch.llm_stability_score is not None else (branch.stability_score or 50.0)
            computed = compute_stability_score(branch)
            branch.llm_stability_score = llm_score
            branch.computed_stability_score = computed
            branch.final_stability_score = round((0.6 * computed) + (0.4 * llm_score), 2)
            branch.stability_score = branch.final_stability_score
            branch.risk_clusters = sorted(branch.risk_clusters, key=lambda r: r.severity_level, reverse=True)
        result.audit.embedding_docs_used = len(retrieved)
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
