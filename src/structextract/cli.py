"""CLI for StructExtract."""

from __future__ import annotations

import json
from pathlib import Path

import click
from rich.console import Console

from .baseline import extract as baseline_extract
from .eval import aggregate, record_score

console = Console()


def _load_jsonl(path):
    out = []
    with Path(path).open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


@click.group()
def main():
    """StructExtract: structured extraction from messy text."""


@main.command()
@click.option("--data", "data_path", required=True, type=click.Path(exists=True))
@click.option("--n", type=int, default=50)
def baseline_eval(data_path, n):
    """Evaluate the regex baseline on the dataset."""
    rows = _load_jsonl(data_path)[:n]
    scores = []
    for r in rows:
        pred = baseline_extract(r["text"]).to_canonical() if hasattr(baseline_extract(r["text"]), "to_canonical") else baseline_extract(r["text"]).__dict__
        # normalize
        pred = baseline_extract(r["text"]).to_canonical()
        sc = record_score(pred, r["gold"])
        sc["gold"] = r["gold"]
        sc["json_valid"] = True
        scores.append(sc)
    m = aggregate(scores)
    console.print_json(data=m)


@main.command()
@click.option("--text", required=True)
def extract(text):
    """Extract fields from a single text using the regex baseline."""
    rec = baseline_extract(text)
    console.print_json(data=rec.to_canonical())


@main.command()
@click.option("--data", "data_path", required=True, type=click.Path(exists=True))
@click.option("--out", "out_path", type=click.Path(), default="data/synthetic.jsonl")
@click.option("--n", type=int, default=300)
def generate(data_path, out_path, n):
    """Generate synthetic dataset."""
    from .generate import write_jsonl

    write_jsonl(out_path, n=n)
    console.print(f"[green]Generated {n} records to {out_path}[/green]")


if __name__ == "__main__":
    main()