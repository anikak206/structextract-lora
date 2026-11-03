"""Extraction schema."""

from __future__ import annotations

from pydantic import BaseModel


class CaseRecord(BaseModel):
    case_number: str | None = None
    court: str | None = None
    date: str | None = None
    parties: str | None = None
    amount: str | None = None
    outcome: str | None = None

    def to_canonical(self) -> dict:
        return {k: (v if v is not None else "") for k, v in self.model_dump().items()}


FIELDS = list(CaseRecord.model_fields.keys())