from click.testing import CliRunner

from structextract.cli import main


def test_baseline_eval():
    runner = CliRunner()
    res = runner.invoke(main, ["baseline-eval", "--data", "data/synthetic.jsonl", "--n", "10"])
    assert res.exit_code == 0, res.output


def test_extract():
    runner = CliRunner()
    res = runner.invoke(main, ["extract", "--text", "Case WP/1/2023 on 01/01/2023 in Supreme Court dismissed."])
    assert res.exit_code == 0, res.output