"""QLoRA fine-tuning script (requires torch/transformers/peft)."""

from __future__ import annotations

import json
from pathlib import Path

try:
    import torch
    from datasets import Dataset
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        DataCollatorForLanguageModeling,
        Trainer,
        TrainingArguments,
    )
    _DEPS_OK = True
except (ImportError, RuntimeError):
    _DEPS_OK = False


def _format_example(ex: dict) -> str:
    from .schema import CaseRecord

    gold = ex["gold"]
    rec = CaseRecord(**gold)
    return (f"### Instruction:\nExtract structured fields as JSON.\n\n"
            f"### Input:\n{ex['text']}\n\n"
            f"### Output:\n{json.dumps(rec.to_canonical())}")


def load_data(path: str):
    rows = []
    with Path(path).open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def train(data_path: str, model_name: str = "Qwen/Qwen2.5-1.5B-Instruct",
          output_dir: str = "outputs/lora", epochs: int = 3,
          batch_size: int = 4, lr: float = 2e-4, lora_r: int = 16):
    if not _DEPS_OK:
        raise RuntimeError("Training deps not installed. pip install structextract-lora[train]")
    rows = load_data(data_path)
    texts = [_format_example(r) for r in rows]

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                             bnb_4bit_compute_dtype=torch.float16)
    model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb,
                                                device_map="auto", trust_remote_code=True)
    model = prepare_model_for_kbit_training(model)
    lora_cfg = LoraConfig(r=lora_r, lora_alpha=32, target_modules=["q_proj", "v_proj"],
                          lora_dropout=0.05, bias="none", task_type="CAUSAL_LM")
    model = get_peft_model(model, lora_cfg)

    ds = Dataset.from_dict({"text": texts})

    def tok_fn(batch):
        return tokenizer(batch["text"], truncation=True, max_length=512, padding="max_length")

    ds = ds.map(tok_fn, batched=True, remove_columns=["text"])

    args = TrainingArguments(
        output_dir=output_dir, num_train_epochs=epochs,
        per_device_train_batch_size=batch_size, learning_rate=lr,
        logging_steps=10, save_strategy="epoch", fp16=True,
        report_to="none",
    )
    trainer = Trainer(model=model, args=args, train_dataset=ds,
                      data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False))
    trainer.train()
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Saved adapter to {output_dir}")