"""Inference helpers."""

from __future__ import annotations

from typing import Any

from .prompt import parse_llm_output


def extract_with_model(text: str, model, tokenizer, max_new_tokens: int = 128) -> dict[str, Any] | None:
    """Run a fine-tuned (or base) causal LM to extract JSON."""
    import torch

    prompt = f"### Instruction:\nExtract structured fields as JSON.\n\n### Input:\n{text}\n\n### Output:\n"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    decoded = tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    return parse_llm_output(decoded)