import pytest
from pydantic import ValidationError

from app.schemas import SimulationResult


def test_schema_rejects_too_many_branches():
    payload = {
        "decision_id": "x",
        "input_summary": "s",
        "assumptions": [],
        "branches": [],
        "overall_recommendation": "r",
        "audit": {"model_id": "m"},
    }
    for i in range(7):
        payload["branches"].append(
            {
                "branch_name": f"b{i}",
                "narrative": "n",
                "key_events": ["e"],
                "KPIs": {"revenue": 1, "margin": 1, "burn": 1, "headcount": 1, "churn": 1},
                "risk_clusters": [{"tag": "t", "severity": "low"}],
                "stress_points": [{"resource": "cash", "threshold": "x"}],
                "failure_triggers": [{"condition": "if", "impact": "then"}],
                "mitigations": [{"rank": 1, "action": "do"}],
                "stability_score": 50,
            }
        )
    with pytest.raises(ValidationError):
        SimulationResult.model_validate(payload)

