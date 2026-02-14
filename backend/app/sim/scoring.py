from app.schemas import Branch


def compute_stability_score(branch: Branch) -> float:
    score = 70.0

    # Penalize high-severity risks.
    for risk in branch.risk_clusters:
        score -= risk.severity_level * 3.5

    # Penalize too many failure triggers.
    if len(branch.failure_triggers) > 2:
        score -= (len(branch.failure_triggers) - 2) * 5.0

    # Penalize negative margin or clear revenue decline signals.
    if branch.kpis.margin < 0:
        score -= 12.0
    if _has_revenue_decline(branch):
        score -= 8.0

    # Boost strong mitigations.
    strong_mitigations = [m for m in branch.mitigations if m.rank <= 2 and len(m.action.strip()) >= 18]
    score += min(12.0, len(strong_mitigations) * 4.0)

    # Boost diversification across risk tags.
    distinct_tags = {r.tag.strip().lower() for r in branch.risk_clusters if r.tag.strip()}
    if len(distinct_tags) >= 2:
        score += 6.0

    # Boost manageable stress thresholds.
    manageable = sum(1 for s in branch.stress_points if _is_manageable_threshold(s.threshold))
    score += min(8.0, manageable * 2.0)

    return round(max(0.0, min(100.0, score)), 2)


def _has_revenue_decline(branch: Branch) -> bool:
    text = f"{branch.narrative} {' '.join(branch.key_events)}".lower()
    decline_markers = ("revenue decline", "revenue drop", "decline", "down", "miss")
    return any(marker in text for marker in decline_markers)


def _is_manageable_threshold(threshold: str) -> bool:
    t = threshold.lower()
    manageable_markers = ("<", "<=", "less than", "below", "under")
    return any(marker in t for marker in manageable_markers)

