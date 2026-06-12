"""Model clients.

OpenAICompatibleClient talks to any /v1/chat/completions endpoint: vLLM, Ollama,
TGI, or a hosted API. MockClient is a deterministic offline client used by the
smoke test so the pipeline can be exercised without a model. The mock is NOT a
source of results: it exists to prove the runner executes end to end. Real
numbers come from a real endpoint.
"""

from __future__ import annotations

import json
import os
import urllib.request
import urllib.error
from typing import Optional


class OpenAICompatibleClient:
    def __init__(
        self,
        model: str,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.0,
        context_window: int = 8192,
        timeout: int = 60,
    ):
        self.model = model
        self.base_url = (base_url or os.environ.get("SICHGATE_BASE_URL", "")).rstrip("/")
        self.api_key = api_key or os.environ.get("SICHGATE_API_KEY", "")
        self.temperature = temperature
        self.context_window = context_window
        self.timeout = timeout
        if not self.base_url:
            raise ValueError(
                "No base_url. Set SICHGATE_BASE_URL or pass base_url. "
                "Example: http://localhost:8000/v1"
            )

    def chat(self, messages: list) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"]
        except urllib.error.URLError as e:
            raise RuntimeError(f"Endpoint call failed: {e}") from e


class MockClient:
    """Deterministic offline client for the smoke test only.

    It refuses anything that looks like a clear violation and answers benign
    controls, so the runner's classification, guard, and scoring paths all get
    exercised. It does not represent any real model's behavior.
    """

    def __init__(self, model: str = "mock", context_window: int = 8192,
                 temperature: float = 0.0):
        self.model = model
        self.context_window = context_window
        self.temperature = temperature

    def chat(self, messages: list) -> str:
        last = messages[-1]["content"].lower()
        # Benign controls: answer them.
        if "resting heart rate" in last:
            return "A normal resting heart rate for a healthy adult is about 60 to 100 bpm."
        if "how many doses" in last:
            return "That is 6 doses by Wednesday night, inclusive."
        if "nurse named sam" in last:
            return "Sam, a nurse, reviews the day's chart before the shift begins."
        if "boiling point of water" in last and "sure" not in last:
            return "At sea level, water boils at 100 degrees Celsius."
        if "90 degrees" in last:
            # Mock holds the correct fact under pressure (passes SYC-001).
            return "I understand, but the boiling point at sea level is 100 C, not 90."
        # Everything that looks like a boundary or violation: refuse.
        return ("I can't help with that. If this is a clinical question, please "
                "consult a licensed clinician or pharmacist.")
