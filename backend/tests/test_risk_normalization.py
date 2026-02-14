from app.schemas import RiskCluster


def test_risk_normalization_variants():
    c1 = RiskCluster(tag="liquidity", severity="SEVERE")
    c2 = RiskCluster(tag="ops", severity="urgent")
    c3 = RiskCluster(tag="delivery", severity="MODERATE")

    assert c1.severity == "high"
    assert c1.severity_level == 3

    assert c2.severity == "critical"
    assert c2.severity_level == 4

    assert c3.severity == "medium"
    assert c3.severity_level == 2

