import json
import logging
import time
from typing import Any

import boto3
from botocore.config import Config
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import get_settings
from app.providers.interfaces import LLMProvider, LLMResponse
from app.schemas import AuditMeta, SimulationResult
from app.sim.prompt_builder import PromptBuilder

logger = logging.getLogger(__name__)


class NovaLiteClient(LLMProvider):
    def __init__(self) -> None:
        settings = get_settings()
        session_kwargs: dict[str, Any] = {"region_name": settings.aws_region}
        if settings.aws_profile:
            session_kwargs["profile_name"] = settings.aws_profile
        session = boto3.Session(**session_kwargs)
        self._client = session.client("bedrock-runtime", config=Config(retries={"max_attempts": 3}))
        self._model_id = settings.bedrock_model_id_nova_lite
        self._prompt_builder = PromptBuilder()

    @retry(wait=wait_exponential(multiplier=1, min=1, max=8), stop=stop_after_attempt(3), reraise=True)
    def generate_json(self, prompt: str) -> LLMResponse:
        start = time.perf_counter()
        body = {
            "messages": [{"role": "user", "content": [{"text": prompt}]}],
            "inferenceConfig": {"maxTokens": 1800, "temperature": 0.2, "topP": 0.9},
        }
        logger.info("bedrock_request", extra={"model_id": self._model_id, "body_keys": list(body.keys())})
        resp = self._client.converse(modelId=self._model_id, **body)
        latency_ms = int((time.perf_counter() - start) * 1000)
        output_message = resp.get("output", {}).get("message", {}).get("content", [])
        text = next((item.get("text", "") for item in output_message if "text" in item), "{}")
        usage = resp.get("usage", {})
        logger.info("bedrock_response", extra={"model_id": self._model_id, "latency_ms": latency_ms})
        return LLMResponse(
            content=text,
            model_id=self._model_id,
            latency_ms=latency_ms,
            tokens_input=usage.get("inputTokens"),
            tokens_output=usage.get("outputTokens"),
        )

    def simulate_decision(self, prompt: str, context: list[str], constraints: dict[str, Any]) -> SimulationResult:
        _ = context, constraints
        primary = self.generate_json(prompt)
        try:
            result = SimulationResult.model_validate_json(primary.content)
        except Exception as exc:
            repair_prompt = self._prompt_builder.build_repair(primary.content, str(exc))
            repaired = self.generate_json(repair_prompt)
            result = SimulationResult.model_validate_json(repaired.content)
            result.audit = AuditMeta(
                model_id=repaired.model_id,
                latency_ms=primary.latency_ms + repaired.latency_ms,
                tokens_input=(primary.tokens_input or 0) + (repaired.tokens_input or 0),
                tokens_output=(primary.tokens_output or 0) + (repaired.tokens_output or 0),
            )
            return result
        result.audit = AuditMeta(
            model_id=primary.model_id,
            latency_ms=primary.latency_ms,
            tokens_input=primary.tokens_input,
            tokens_output=primary.tokens_output,
        )
        return result

