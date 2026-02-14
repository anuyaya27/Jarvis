from app.schemas import Branch, FailureTrigger, KPISet, Mitigation, RiskCluster, StressPoint
from app.sim.scoring import compute_stability_score


def test_stability_scoring_deterministic():
    branch = Branch(
        branch_name="base",
        narrative="Revenue decline risk remains manageable with strong controls.",
        key_events=["Revenue decline in Q2", "Mitigation gates activated"],
        KPIs=KPISet(revenue=120.0, margin=-2.0, burn=12.0, headcount=900, churn=5.0),
        risk_clusters=[
            RiskCluster(tag="liquidity", severity="CRITICAL"),
            RiskCluster(tag="integration", severity="moderate"),
            RiskCluster(tag="regulatory", severity="high"),
        ],
        stress_points=[
            StressPoint(resource="cash runway", threshold="< 9 months"),
            StressPoint(resource="debt", threshold="<= 3.0x leverage"),
        ],
        failure_triggers=[
            FailureTrigger(condition="if covenant breached", impact="penalty"),
            FailureTrigger(condition="if retention drops", impact="delay"),
            FailureTrigger(condition="if financing tightens", impact="cost spike"),
        ],
        mitigations=[
            Mitigation(rank=1, action="Pre-negotiate contingency credit line before close"),
            Mitigation(rank=2, action="Introduce staged integration gates with weekly KPI reviews"),
        ],
        stability_score=55,
    )

    score_1 = compute_stability_score(branch)
    score_2 = compute_stability_score(branch)
    assert score_1 == score_2
    assert 0.0 <= score_1 <= 100.0

