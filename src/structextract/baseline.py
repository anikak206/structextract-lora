"""Classical (regex) baseline extractor."""

from __future__ import annotations

import re

from .schema import CaseRecord

_DATE_RE = re.compile(r"\b(\d{1,2}[\-/]\d{1,2}[\-/]\d{2,4}|\d{4}-\d{2}-\d{2})\b")
_AMOUNT_RE = re.compile(r"(?:Rs\.?|INR|₹)\s*[\d,]+(?:\.\d+)?", re.IGNORECASE)
_CASE_RE = re.compile(r"\b(?:Case|WP|Crl\.?\s*A\.?|SLP|Appeal)\s*(?:No\.?)?\s*[:#]?\s*[\w/\-]+\b", re.IGNORECASE)
_COURT_RE = re.compile(r"\b(Supreme Court|High Court|District Court|Sessions Court|Tribunal)\b", re.IGNORECASE)
_OUTCOME_RE = re.compile(r"\b(dismissed|allowed|granted|rejected|acquitted|convicted|upheld|quashed)\b", re.IGNORECASE)


def extract(text: str) -> CaseRecord:
    date = _DATE_RE.search(text)
    amount = _AMOUNT_RE.search(text)
    case = _CASE_RE.search(text)
    court = _COURT_RE.search(text)
    outcome = _OUTCOME_RE.search(text)
    # parties: heuristic "X v. Y" or "X vs Y"
    parties_m = re.search(r"([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\s+v\.?\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)", text)
    parties = parties_m.group(0) if parties_m else None
    return CaseRecord(
        case_number=case.group(0) if case else None,
        court=court.group(0) if court else None,
        date=date.group(0) if date else None,
        parties=parties,
        amount=amount.group(0) if amount else None,
        outcome=outcome.group(0).lower() if outcome else None,
    )