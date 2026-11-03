from structextract.schema import FIELDS, CaseRecord


def test_schema_fields():
    assert "case_number" in FIELDS
    assert len(FIELDS) == 6


def test_canonical():
    rec = CaseRecord(case_number="WP/1", court=None)
    c = rec.to_canonical()
    assert c["court"] == ""
    assert c["case_number"] == "WP/1"