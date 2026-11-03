from structextract.baseline import extract
from structextract.schema import CaseRecord


def test_baseline_extracts_date():
    text = "Case WP/123/2023 heard on 12/05/2023 in Supreme Court. Result: dismissed."
    rec = extract(text)
    assert rec.date == "12/05/2023"
    assert rec.court == "Supreme Court"
    assert rec.outcome == "dismissed"


def test_baseline_returns_model():
    rec = extract("no info here")
    assert isinstance(rec, CaseRecord)