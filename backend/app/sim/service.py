import json

from app.kb.service import KBService
from app.providers.interfaces import LLMProvider
from app.schemas import DecisionSpec, RecommendedPath, SimulateRequest, SimulationResult, TopRisk
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
        result.top_3_risks = self._build_top_risks(result)
        result.recommended_path = self._build_recommended_path(result)
        result.executive_summary = self._truncate_words(
            result.executive_summary or self._build_executive_summary(result),
            max_words=150,
        )
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

    def _build_top_risks(self, result: SimulationResult) -> list[TopRisk]:
        flattened: list[TopRisk] = []
        for branch in result.branches:
            for risk in branch.risk_clusters:
                flattened.append(
                    TopRisk(
                        branch_name=branch.branch_name,
                        tag=risk.tag,
                        severity=risk.severity,
                        severity_level=risk.severity_level,
                        confidence=risk.confidence,
                    )
                )
        flattened.sort(key=lambda r: (r.severity_level, r.confidence or 0.0), reverse=True)
        return flattened[:3]

    def _build_recommended_path(self, result: SimulationResult) -> RecommendedPath | None:
        if not result.branches:
            return None
        best = max(result.branches, key=lambda b: b.final_stability_score or 0.0)
        reasoning = (
            f"{best.branch_name} is preferred because it has the strongest final stability score "
            "after deterministic risk adjustments. The branch has comparatively manageable stress points "
            "and mitigation coverage. Execute with milestone-based controls and monitoring on failure triggers."
        )
        return RecommendedPath(branch_name=best.branch_name, reasoning=reasoning)

    def _build_executive_summary(self, result: SimulationResult) -> str:
        best = max(result.branches, key=lambda b: b.final_stability_score or 0.0) if result.branches else None
        if not best:
            return "No branches generated."
        top_tags = sorted({r.tag for r in best.risk_clusters})
        return (
            f"Simulation generated {len(result.branches)} branches for the stated decision. "
            f"The leading branch is {best.branch_name} with final stability {best.final_stability_score}. "
            f"Top risks concentrate around {', '.join(top_tags) or 'execution'}; "
            "mitigations should be front-loaded with KPI gates and liquidity safeguards."
        )

    @staticmethod
    def _truncate_words(text: str, max_words: int) -> str:
        words = text.split()
        if len(words) <= max_words:
            return text
        return " ".join(words[:max_words]).strip()


def limit_branches(branches: list, max_branches: int = 6) -> list:
    return branches[:max_branches]
