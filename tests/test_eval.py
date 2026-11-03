from structextract.eval import aggregate, json_valid, record_score
from structextract.prompt import parse_llm_output


def test_json_valid():
    assert json_valid('{"a": 1}') is True
    assert json_valid("not json") is False


def test_record_score():
    gold = {"case_number": "WP/1/2023", "court": "Supreme Court", "date": "01/01/2023",
            "parties": None, "amount": None, "outcome": "dismissed"}
    pred = {"case_number": "WP/1/2023", "court": "Supreme Court", "date": "01/01/2023",
            "parties": None, "amount": None, "outcome": "dismissed"}
    sc = record_score(pred, gold)
    assert sc["record_accuracy"] == 1.0


def test_aggregate():
    gold = {"case_number": "WP/1/2023", "court": "Supreme Court", "date": "01/01/2023",
            "parties": None, "amount": None, "outcome": "dismissed"}
    pred = {"case_number": "WP/1/2023", "court": "Supreme Court", "date": "01/01/2023",
            "parties": None, "amount": None, "outcome": "dismissed"}
    sc = record_score(pred, gold)
    sc["gold"] = gold
    sc["json_valid"] = True
    m = aggregate([sc])
    assert m["n_records"] == 1
    assert m["json_validity_rate"] == 1.0


def test_parse_llm_output():
    raw = '{"case_number": "WP/1/2023", "court": "Supreme Court", "date": "01/01/2023", "parties": null, "amount": null, "outcome": "dismissed"}'
    out = parse_llm_output(raw)
    assert out is not None
    assert out["court"] == "Supreme Court"


def test_parse_llm_output_bad():
    assert parse_llm_output("not json") is None