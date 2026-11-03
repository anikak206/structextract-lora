from structextract.prompt import few_shot_prompt, parse_llm_output, zero_shot_prompt


def test_zero_shot_contains_text():
    p = zero_shot_prompt("hello world")
    assert "hello world" in p
    assert "JSON" in p


def test_few_shot():
    ex = [{"text": "t1", "gold": {"case_number": "X", "court": None, "date": None,
            "parties": None, "amount": None, "outcome": None}}]
    p = few_shot_prompt("q", ex)
    assert "t1" in p


def test_parse_valid():
    raw = '{"case_number": "X", "court": null, "date": null, "parties": null, "amount": null, "outcome": null}'
    out = parse_llm_output(raw)
    assert out is not None
    assert out["case_number"] == "X"