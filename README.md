# AI Log Explainer 🛠️

A minimalist CLI tool that turns raw JSON‑formatted service logs into short, human‑friendly explanations using the OpenAI Chat Completions API.

## Quick start

```bash
# 1.  Clone or download the zip, then:
cd ai_log_explainer
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2.  Make your OpenAI key available
export OPENAI_API_KEY="sk‑..."

# 3.  Pipe logs or pass a file
cat sample_logs.jsonl | python main.py
#  – or –
python main.py --logfile sample_logs.jsonl --model gpt-4o-mini --lines 150
```

## What it does
1. Reads newline‑delimited JSON log entries (from a file or **stdin**).
2. Keeps the last *N* lines (default = 120) to stay within token limits.
3. Sends them to the Chat Completions endpoint with a purpose‑built
   SRE prompt.
4. Prints the resulting one‑ or two‑sentence root‑cause analysis /
   recommendation.

## Configuration

* `OPENAI_API_KEY` — must be set as env‑var **or** put in `config.toml`
  (see `config.example.toml`).
* `--model`      — any Chat model your key can access (`gpt-4o`, `gpt-4o-mini`, etc).
* `--lines`      — how many recent log entries to include (default 120).

## Files

```
ai_log_explainer/
├── main.py               # CLI entry‑point
├── requirements.txt      # pip deps
├── config.example.toml   # optional key storage
├── sample_logs.jsonl     # toy data for a dry‑run
└── README.md             # this doc
```

## Cost ⚠️
Each run consumes OpenAI tokens for both prompt (your logs) and
completion. When calling large models with many log lines the cost
can add up quickly.

---
MIT‑licensed — happy debugging!
