from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator


class KPISet(BaseModel):
    revenue: float
    margin: float
    burn: float
    headcount: int
    churn: float


class RiskCluster(BaseModel):
    tag: str
    severity: Literal["low", "medium", "high", "critical"]


class StressPoint(BaseModel):
    resource: str
    threshold: str


class FailureTrigger(BaseModel):
    condition: str
    impact: str


class Mitigation(BaseModel):
    rank: int = Field(ge=1)
    action: str


class Branch(BaseModel):
    branch_name: str
    narrative: str
    key_events: list[str]
    kpis: KPISet = Field(alias="KPIs")
    risk_clusters: list[RiskCluster]
    stress_points: list[StressPoint]
    failure_triggers: list[FailureTrigger]
    mitigations: list[Mitigation]
    stability_score: int = Field(ge=0, le=100)


class AuditMeta(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_id: str
    latency_ms: int = 0
    tokens_input: int | None = None
    tokens_output: int | None = None


class SimulationResult(BaseModel):
    decision_id: str = Field(default_factory=lambda: str(uuid4()))
    input_summary: str
    assumptions: list[str]
    branches: list[Branch] = Field(max_length=6)
    overall_recommendation: str
    audit: AuditMeta

    @model_validator(mode="after")
    def ensure_branch_limit(self):
        if len(self.branches) > 6:
            self.branches = self.branches[:6]
        return self


class SimulateRequest(BaseModel):
    decision_text: str | None = None
    transcript: str | None = None
    context_doc_ids: list[str] = Field(default_factory=list)
    constraints: dict[str, str | int | float | bool | list[str]] = Field(default_factory=dict)

    @model_validator(mode="after")
    def require_text_or_transcript(self):
        if not self.decision_text and not self.transcript:
            raise ValueError("decision_text or transcript is required")
        return self


class DecisionSpec(BaseModel):
    decision_title: str
    objective: str
    options: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    time_horizon: str
    market_context: str
    key_assumptions: list[str] = Field(default_factory=list)


class DecisionSpecRequest(BaseModel):
    decision_text: str | None = None
    transcript: str | None = None

    @model_validator(mode="after")
    def require_source_text(self):
        if not self.decision_text and not self.transcript:
            raise ValueError("decision_text or transcript is required")
        return self


class KBQueryRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=20)


class KBMatch(BaseModel):
    text: str
    source: str
    score: float


class KBQueryResponse(BaseModel):
    matches: list[KBMatch]


class KBUploadResponse(BaseModel):
    doc_id: str
    chunks: int


class VoiceSessionResponse(BaseModel):
    session_id: str


class PlaybookRequest(BaseModel):
    name: str
    payload: dict = Field(default_factory=dict)
