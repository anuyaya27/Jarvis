import json
import logging
import random
import time
from typing import Any

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

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

    def generate_json(self, prompt: str) -> LLMResponse:
        payload = {
            "messages": [{"role": "user", "content": [{"text": prompt}]}],
            "inferenceConfig": {"maxTokens": 1800, "temperature": 0.2, "topP": 0.9},
        }
        max_attempts = 3
        retry_count = 0
        last_exc: Exception | None = None
        for attempt in range(1, max_attempts + 1):
            start = time.perf_counter()
            logger.info("bedrock_request", extra={"model_id": self._model_id, "prompt_chars": len(prompt), "attempt": attempt})
            try:
                try:
                    resp = self._client.converse(modelId=self._model_id, **payload)
                    text, usage = self._extract_converse_payload(resp)
                except (AttributeError, ClientError) as exc:
                    if isinstance(exc, ClientError):
                        code = exc.response.get("Error", {}).get("Code", "")
                        if code not in {"UnknownOperationException", "ValidationException"}:
                            raise
                    resp = self._client.invoke_model(modelId=self._model_id, body=json.dumps(payload))
                    invoke_payload = json.loads(resp["body"].read())
                    text, usage = self._extract_invoke_payload(invoke_payload)
                latency_ms = int((time.perf_counter() - start) * 1000)
                json_text = self._extract_first_json(text) or "{}"
                logger.info("bedrock_response", extra={"model_id": self._model_id, "latency_ms": latency_ms, "attempt": attempt})
                return LLMResponse(
                    content=json_text,
                    model_id=self._model_id,
                    latency_ms=latency_ms,
                    tokens_input=usage.get("inputTokens"),
                    tokens_output=usage.get("outputTokens"),
                    retry_count=retry_count,
                )
            except Exception as exc:
                last_exc = exc
                if attempt >= max_attempts:
                    break
                retry_count += 1
                sleep_s = min(8.0, (2 ** (attempt - 1)) + random.uniform(0.0, 0.3))
                time.sleep(sleep_s)
        assert last_exc is not None
        raise last_exc

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
                retry_count=primary.retry_count + repaired.retry_count,
                used_repair_pass=True,
                used_mock=False,
            )
            return result
        result.audit = AuditMeta(
            model_id=primary.model_id,
            latency_ms=primary.latency_ms,
            tokens_input=primary.tokens_input,
            tokens_output=primary.tokens_output,
            retry_count=primary.retry_count,
            used_repair_pass=False,
            used_mock=False,
        )
        return result

    @staticmethod
    def _extract_converse_payload(resp: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        output_message = resp.get("output", {}).get("message", {}).get("content", [])
        text = next((item.get("text", "") for item in output_message if "text" in item), "{}")
        usage = resp.get("usage", {})
        return text, usage

    @staticmethod
    def _extract_invoke_payload(payload: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        if "output" in payload and "message" in payload.get("output", {}):
            output_message = payload.get("output", {}).get("message", {}).get("content", [])
            text = next((item.get("text", "") for item in output_message if "text" in item), "{}")
        elif "content" in payload and isinstance(payload["content"], list):
            text = "".join(part.get("text", "") for part in payload["content"] if isinstance(part, dict))
        else:
            text = payload.get("generation", payload.get("outputText", "{}"))
        usage = payload.get("usage", {})
        return text, usage

    @staticmethod
    def _extract_first_json(text: str) -> str | None:
        decoder = json.JSONDecoder()
        for idx, ch in enumerate(text):
            if ch != "{":
                continue
            try:
                obj, _ = decoder.raw_decode(text[idx:])
                return json.dumps(obj)
            except Exception:
                continue
        return None
