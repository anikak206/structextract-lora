"""Evaluation metrics for structured extraction."""

from __future__ import annotations

import json
from typing import Any

from .schema import FIELDS


def json_valid(pred_str: str) -> bool:
    try:
        json.loads(pred_str)
        return True
    except (ValueError, TypeError):
        return False


def field_exact_match(pred: dict, gold: dict) -> dict[str, bool]:
    out = {}
    for f in FIELDS:
        p = (pred.get(f) or "").strip().lower()
        g = (gold.get(f) or "").strip().lower()
        out[f] = p == g and g != ""
    return out


def record_score(pred: dict, gold: dict) -> dict[str, Any]:
    fem = field_exact_match(pred, gold)
    len(FIELDS)
    correct = sum(1 for v in fem.values() if v)
    # only count fields present in gold
    gold_present = sum(1 for f in FIELDS if (gold.get(f) or "").strip() != "")
    acc = correct / gold_present if gold_present > 0 else 1.0
    return {"field_exact_match": fem, "correct_fields": correct,
            "gold_fields": gold_present, "record_accuracy": round(acc, 4)}


def aggregate(scores: list[dict[str, Any]]) -> dict[str, Any]:
    if not scores:
        return {}
    n = len(scores)
    field_correct = {f: 0 for f in FIELDS}
    field_total = {f: 0 for f in FIELDS}
    rec_accs = []
    json_valid_count = 0
    for s in scores:
        for f in FIELDS:
            gv = s.get("gold", {}).get(f)
            if gv is not None and str(gv).strip() != "":
                field_total[f] += 1
                if s["field_exact_match"].get(f):
                    field_correct[f] += 1
        rec_accs.append(s["record_accuracy"])
        if s.get("json_valid"):
            json_valid_count += 1
    field_f1: dict[str, float | None] = {}
    for f in FIELDS:
        if field_total[f] > 0:
            field_f1[f] = round(field_correct[f] / field_total[f], 4)
        else:
            field_f1[f] = None
    return {
        "n_records": n,
        "json_validity_rate": round(json_valid_count / n, 4),
        "mean_record_accuracy": round(sum(rec_accs) / n, 4),
        "field_exact_match": field_f1,
        "total_correct_fields": sum(s["correct_fields"] for s in scores),
        "total_gold_fields": sum(s["gold_fields"] for s in scores),
    }