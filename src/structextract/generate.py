"""Generate synthetic messy extraction dataset."""

from __future__ import annotations

import json
import random
from pathlib import Path

NAMES = ["Ramesh Kumar", "Sita Devi", "Anil Sharma", "Priya Nair", "Mohammed Ali",
         "Geeta Rao", "Vikram Singh", "Lakshmi Iyer"]
COURTS = ["Supreme Court", "Delhi High Court", "Bombay High Court", "Madras High Court"]
OUTCOMES = ["dismissed", "allowed", "granted", "rejected", "upheld", "quashed"]
PARTIES_TPL = ["{a} v. {b}", "{a} vs {b}", "{a} and another v. {b}"]


def make_one(rng: random.Random) -> dict:
    rng.choice(NAMES)
    court = rng.choice(COURTS)
    date = f"{rng.randint(1,28):02d}/{rng.randint(1,12):02d}/{rng.choice([2022,2023,2024])}"
    amount = f"Rs. {rng.randint(10000,999999):,}"
    case_no = f"WP/{rng.randint(100,999)}/{rng.randint(2020,2024)}"
    outcome = rng.choice(OUTCOMES)
    a, b = rng.choice(NAMES), rng.choice(NAMES)
    parties = rng.choice(PARTIES_TPL).format(a=a, b=b)

    # messy text variants
    templates = [
        "Case {case} heard on {date} in {court}. {parties}. Amount involved {amount}. The petition was {outcome}.",
        "{court} - matter no {case}, decided {date}. Parties: {parties}. Claim of {amount}. Result: {outcome}.",
        "On {date}, {court} dismissed/allowed... {parties} (case {case}) involving {amount}; final outcome {outcome}.",
    ]
    text = rng.choice(templates).format(case=case_no, date=date, court=court, parties=parties,
                                        amount=amount, outcome=outcome)
    # add noise
    if rng.random() < 0.3:
        text = text.upper() if rng.random() < 0.5 else text
    if rng.random() < 0.2:
        text = text.replace(" ", "  ")

    gold = {
        "case_number": case_no,
        "court": court,
        "date": date,
        "parties": parties,
        "amount": amount,
        "outcome": outcome,
    }
    return {"text": text, "gold": gold}


def generate(n: int = 300, seed: int = 42) -> list[dict]:
    rng = random.Random(seed)
    return [make_one(rng) for _ in range(n)]


def write_jsonl(path: str | Path, n: int = 300, seed: int = 42):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    rows = generate(n, seed)
    with Path(path).open("w", encoding="utf-8") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    return len(rows)