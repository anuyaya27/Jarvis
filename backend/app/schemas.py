from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, model_validator


SEVERITY_MAP: dict[str, tuple[str, int]] = {
    "low": ("low", 1),
    "minor": ("low", 1),
    "medium": ("medium", 2),
    "moderate": ("medium", 2),
    "high": ("high", 3),
    "severe": ("high", 3),
    "critical": ("critical", 4),
    "urgent": ("critical", 4),
}


class KPISet(BaseModel):
    revenue: float
    margin: float
    burn: float
    headcount: int
    churn: float


class RiskCluster(BaseModel):
    tag: str
    severity: Literal["low", "medium", "high", "critical"]
    severity_level: int = Field(default=1, ge=1, le=4)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)

    @field_validator("severity", mode="before")
    @classmethod
    def normalize_severity(cls, value: str) -> str:
        norm = (value or "").strip().lower()
        if norm in SEVERITY_MAP:
            return SEVERITY_MAP[norm][0]
        return "medium"

    @model_validator(mode="after")
    def set_severity_level(self):
        self.severity_level = SEVERITY_MAP[self.severity][1]
        return self


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
    llm_stability_score: float | None = Field(default=None, ge=0, le=100)
    computed_stability_score: float | None = Field(default=None, ge=0, le=100)
    final_stability_score: float | None = Field(default=None, ge=0, le=100)
    stability_score: float | None = Field(default=None, ge=0, le=100)

    @model_validator(mode="after")
    def map_deprecated_stability_score(self):
        if self.llm_stability_score is None and self.stability_score is not None:
            self.llm_stability_score = self.stability_score
        if self.final_stability_score is None:
            if self.computed_stability_score is not None and self.llm_stability_score is not None:
                self.final_stability_score = round(0.6 * self.computed_stability_score + 0.4 * self.llm_stability_score, 2)
            elif self.llm_stability_score is not None:
                self.final_stability_score = self.llm_stability_score
        # Keep backward-compatible field for existing clients.
        self.stability_score = self.final_stability_score
        return self


class AuditMeta(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_id: str
    latency_ms: int = 0
    tokens_input: int | None = None
    tokens_output: int | None = None
    retry_count: int = 0
    used_repair_pass: bool = False
    used_mock: bool = True
    embedding_docs_used: int = 0


class TopRisk(BaseModel):
    branch_name: str
    tag: str
    severity: Literal["low", "medium", "high", "critical"]
    severity_level: int = Field(ge=1, le=4)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class RecommendedPath(BaseModel):
    branch_name: str
    reasoning: str


class SimulationResult(BaseModel):
    decision_id: str = Field(default_factory=lambda: str(uuid4()))
    input_summary: str
    assumptions: list[str]
    branches: list[Branch] = Field(max_length=6)
    executive_summary: str = ""
    top_3_risks: list[TopRisk] = Field(default_factory=list)
    recommended_path: RecommendedPath | None = None
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
