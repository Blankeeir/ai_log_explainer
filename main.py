#!/usr/bin/env python3
"""
ai_log_explainer/main.py
------------------------
Pipe or pass newline‑delimited JSON log entries and receive a concise,
actionable explanation powered by the OpenAI Chat Completion API.

Usage examples
--------------
$ cat logs.jsonl | python main.py
$ python main.py --logfile logs.jsonl --lines 80 --model gpt-4o
"""
import argparse, json, os, sys, textwrap, pathlib, itertools
from datetime import datetime, timezone
from typing import List

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # optional; ignore if not installed
    pass

import openai
from rich.console import Console
from rich.markdown import Markdown

console = Console()

DEFAULT_LINES = 120
DEFAULT_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = textwrap.dedent(
    """        You are a senior Site Reliability Engineer. Given recent JSON‑formatted
    log lines from a production system, identify *in plain English* the most
    likely root cause of any incident and recommend the top one or two
    immediate actions an on‑call engineer should take.
    Respond with **one paragraph (≤ 3 sentences)** – no code blocks.
    """)

def tail_lines(lines: List[str], n: int) -> List[str]:
    """Return the last *n* non‑blank lines."""
    return list(itertools.islice((l for l in lines if l.strip()), max(0, len(lines)-n), len(lines)))

def read_input(path: str | None) -> List[str]:
    if path:
        with open(path, "r", encoding="utf‑8") as fh:
            data = fh.readlines()
    else:
        data = sys.stdin.readlines()
    return data

def build_messages(log_lines: List[str]) -> list[dict]:
    joined = "\n".join(log_lines)
    user_prompt = f"Here are the latest {len(log_lines)} log entries:\n```jsonl\n{joined}\n```\n"                      "Summarise what is going on."
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": user_prompt},
    ]

def main() -> None:
    parser = argparse.ArgumentParser(description="Turn JSON logs into english.")
    parser.add_argument("--logfile", help="Path to newline‑delimited JSON logs (defaults to stdin)")
    parser.add_argument("--lines", type=int, default=DEFAULT_LINES,
                        help=f"How many recent lines to consider (default {DEFAULT_LINES})")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"OpenAI chat model (default {DEFAULT_MODEL})")
    args = parser.parse_args()

    key = os.getenv("OPENAI_API_KEY")
    if not key:
        console.print("[bold red]OPENAI_API_KEY not found[/]. Set env var or config.toml.")
        sys.exit(2)

    all_lines = read_input(args.logfile)
    selected = tail_lines(all_lines, args.lines)
    if not selected:
        console.print("[yellow]No log lines provided.[/]")
        sys.exit(0)

    client = openai.OpenAI(api_key=key)

    messages = build_messages(selected)
    console.print("[dim]Calling OpenAI…[/]", end="\r")
    try:
        completion = client.chat.completions.create(
            model=args.model,
            messages=messages,
            temperature=0.2,
            max_tokens=120,
        )
    except Exception as exc:
        console.print(f"[red]OpenAI call failed:[/] {exc}")
        sys.exit(1)

    answer = completion.choices[0].message.content.strip()
    console.print("\n[bold green]Explanation:[/]")
    console.print(Markdown(answer))

if __name__ == "__main__":
    main()
