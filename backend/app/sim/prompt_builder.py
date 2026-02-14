import json
from typing import Any


class PromptBuilder:
    def build(self, decision_text: str, retrieved_context: list[str], constraints: dict[str, Any]) -> str:
        context_block = "\n".join(f"- {c}" for c in retrieved_context) if retrieved_context else "- none"
        constraints_json = json.dumps(constraints, sort_keys=True)
        return (
            "You are Multiverse Copilot, a high-stakes business strategy simulator.\n"
            "Return JSON only. Do not include markdown.\n"
            "Required output fields: decision_id,input_summary,assumptions,branches,overall_recommendation,audit.\n"
            "Branch instruction: generate diverse futures: optimistic, base, pessimistic, wildcard_1, wildcard_2.\n"
            "Each branch must include: branch_name,narrative,key_events,KPIs,risk_clusters,stress_points,failure_triggers,mitigations,stability_score.\n"
            "Limit branches to max 6.\n"
            f"Decision text: {decision_text}\n"
            f"Retrieved context:\n{context_block}\n"
            f"Constraints: {constraints_json}\n"
            "Produce realistic KPI values and clear mitigations ranked by impact."
        )

    def build_repair(self, broken_json: str, validation_error: str) -> str:
        return (
            "Repair the following JSON to match the required schema exactly. JSON only.\n"
            f"Validation error: {validation_error}\n"
            f"Broken JSON:\n{broken_json}"
        )

