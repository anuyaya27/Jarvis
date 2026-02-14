import json
from typing import Any

import boto3
from botocore.exceptions import ClientError

from app.core.config import get_settings
from app.providers.interfaces import EmbeddingProvider


class NovaEmbeddingsClient(EmbeddingProvider):
    def __init__(self) -> None:
        settings = get_settings()
        session_kwargs: dict[str, Any] = {"region_name": settings.aws_region}
        if settings.aws_profile:
            session_kwargs["profile_name"] = settings.aws_profile
        session = boto3.Session(**session_kwargs)
        self._client = session.client("bedrock-runtime")
        self._model_id = settings.nova_embeddings_model_id

    def _embed_single(self, text: str) -> list[float]:
        body = json.dumps({"inputText": text})
        try:
            response = self._client.invoke_model(
                modelId=self._model_id,
                body=body,
                contentType="application/json",
                accept="application/json",
            )
        except ClientError as exc:
            raise RuntimeError(f"Bedrock embeddings call failed: {exc}") from exc
        payload = json.loads(response["body"].read())
        embedding = payload.get("embedding") or payload.get("embeddings", [None])[0]
        if not embedding:
            raise RuntimeError("Bedrock embeddings response missing embedding vector")
        return embedding

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_single(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed_single(text)
