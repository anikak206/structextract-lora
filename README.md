# StructExtract-LoRA

LoRA/QLoRA fine-tune of a small open model (Qwen 2.5 1.5B) for structured
extraction from messy legal text, compared against prompting (zero-shot /
few-shot) and a classical regex baseline. Built for Gen AI / ML Engineer
internships.

## Measured baseline (regex, 100 records)

| Field | Exact match |
|---|---|
| date | 1.00 |
| amount | 0.83 |
| outcome | 0.76 |
| case_number | 0.35 |
| court | 0.24 |
| parties | 0.19 |
| **Mean record accuracy** | **0.5617** |
| JSON validity | 1.00 |

The LLM fine-tune and prompting results are produced by running the training
notebook on Colab; see `notebooks/train_colab.ipynb`. The eval harness
(`eval.py`) scores any extractor (baseline / prompted / fine-tuned) with the
same metrics so comparisons are apples-to-apples.

## Architecture

```
src/structextract/
  schema.py     Pydantic extraction schema (CaseRecord)
  baseline.py   regex/classical extractor
  prompt.py     zero-shot + few-shot prompts + output parser
  eval.py       field exact-match, record accuracy, JSON validity
  train.py      QLoRA training (optional deps)
  infer.py      inference helper
  generate.py   synthetic dataset generator
  cli.py        baseline-eval / extract / generate
```

## One-command demo

```bash
pip install -e .
structextract baseline-eval --data data/synthetic.jsonl --n 100
structextract extract --text "Case WP/1/2023 on 01/01/2023 in Supreme Court dismissed."
```

## Train (Colab)

See `notebooks/train_colab.ipynb`. Requires a T4 GPU.

## Tests

```bash
pytest -q   # 14 tests
ruff check src tests
mypy src
```

## Limitations

- Synthetic dataset (300 records); real-world messy text is harder.
- LLM fine-tune results depend on Colab run; not committed.
- Baseline regex is weak on case_number/court/parties.

## Resume bullet (X-Y-Z)

> Built StructExtract, a structured-extraction benchmark: implemented a regex
> baseline (record accuracy 0.5617, date 1.0, amount 0.83 on 100 records),
> zero/few-shot prompting, and a QLoRA fine-tuning pipeline (Qwen 2.5 1.5B)
> with a shared eval harness; shipped with 14 tests, CI, Docker, and Colab notebook.

## License

MIT