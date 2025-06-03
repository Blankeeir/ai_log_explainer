# AI Log Explainer

A Python tool that analyzes system logs using OpenAI's API to provide quick explanations and troubleshooting insights for Site Reliability Engineers (SREs).

## Features

- Analyzes JSONL formatted log files
- Uses OpenAI GPT models for intelligent log interpretation
- Provides actionable troubleshooting recommendations
- Focuses on quick incident response and root cause analysis

## Installation

1. Extract the zip file
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## Usage

```bash
python main.py sample_logs.jsonl
```

### Options

- `--model`: Specify OpenAI model (default: gpt-4)

Example:
```bash
python main.py sample_logs.jsonl --model gpt-3.5-turbo
```

## Log Format

The tool expects JSONL (JSON Lines) format where each line is a valid JSON object representing a log entry.

Example log entries:
```json
{"@timestamp": "2025-06-03T02:35:22.191445Z", "level": "CRITICAL", "service": "checkout-api", "msg": "DB connection timeout"}
{"service": "checkout-api", "error": "DB connection timeout", "severity": "SEV-1"}
```

## Sample Output

```
--- Log Entry 1 ---
Original: {"service": "checkout-api", "error": "DB connection timeout", "severity": "SEV-1"}
Analysis: This may be due to a network partition. Check RDS connection status in AWS Console or use psql from EC2.
--------------------------------------------------
```

## Configuration

Set the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Sample Data

The package includes `sample_logs.jsonl` with example log entries for testing.

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection for API calls
