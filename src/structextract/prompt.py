"""Prompting strategies for LLM-based extraction."""

from __future__ import annotations

import json
from typing import Any

from .schema import FIELDS, CaseRecord

SYSTEM = ("You are an information extraction system. Given messy text about a "
          "legal case, output a single JSON object with keys: " + ", ".join(FIELDS) +
          ". Use null for missing fields. Output JSON only, no prose.")


def zero_shot_prompt(text: str) -> str:
    return f"{SYSTEM}\n\nText: {text}\nJSON:"


def few_shot_prompt(text: str, examples: list[dict[str, Any]]) -> str:
    shots = []
    for ex in examples:
        shots.append(f"Text: {ex['text']}\nJSON: {json.dumps(ex['gold'])}")
    shots_str = "\n\n".join(shots)
    return f"{SYSTEM}\n\n{shots_str}\n\nText: {text}\nJSON:"


def parse_llm_output(raw: str) -> dict[str, Any] | None:
    """Parse LLM output into a dict; returns None on failure."""
    raw = raw.strip()
    # strip code fences
    if raw.startswith("```"):
        raw = raw.strip("`").strip()
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()
    try:
        obj = json.loads(raw)
        # validate against schema
        rec = CaseRecord(**obj)
        return rec.to_canonical()
    except (ValueError, TypeError, KeyError):
        return None