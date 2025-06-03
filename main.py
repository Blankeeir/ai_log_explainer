#!/usr/bin/env python3
"""
AI Log Explainer - A tool to analyze system logs using OpenAI API
"""

import json
import sys
import argparse
from typing import Dict, Any, List
import openai
import os
from datetime import datetime

def load_config():
    """Load OpenAI API configuration"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
    
    openai.api_key = api_key
    return openai

def create_system_prompt() -> str:
    """Create the system prompt for log analysis"""
    return """You are an expert Site Reliability Engineer (SRE) analyzing system logs. 
Your job is to quickly explain what's happening in the logs and provide actionable insights.

For each log entry or set of related log entries, provide:
1. A clear, concise explanation of what's happening
2. Potential root causes if there are issues
3. Specific troubleshooting steps or recommendations

Keep responses brief but informative. Focus on actionable insights that help engineers understand and resolve issues quickly.

Examples:
- For database connection timeouts: "This may be due to a network partition. Check RDS connection status in AWS Console or use psql from EC2."
- For payment failures: "Payment declined by issuer. Check with payment processor for specific decline reasons and retry logic."
- For authentication errors: "Token validation failing. Verify JWT secret rotation and check auth service logs."
"""

def analyze_log_entry(client, log_entry: Dict[str, Any]) -> str:
    """Analyze a single log entry using OpenAI API"""
    try:
        log_text = json.dumps(log_entry, indent=2)
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": create_system_prompt()},
                {"role": "user", "content": f"Analyze this log entry:\n{log_text}"}
            ],
            max_tokens=200,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error analyzing log: {str(e)}"

def process_logs(file_path: str) -> None:
    """Process JSONL log file and analyze each entry"""
    try:
        client = load_config()
        
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    log_entry = json.loads(line)
                    print(f"\n--- Log Entry {line_num} ---")
                    print(f"Original: {json.dumps(log_entry)}")
                    
                    analysis = analyze_log_entry(client, log_entry)
                    print(f"Analysis: {analysis}")
                    print("-" * 50)
                    
                except json.JSONDecodeError as e:
                    print(f"Error parsing line {line_num}: {e}")
                    continue
                    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing logs: {e}")
        sys.exit(1)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='AI Log Explainer - Analyze system logs using OpenAI')
    parser.add_argument('log_file', help='Path to JSONL log file')
    parser.add_argument('--model', default='gpt-4', help='OpenAI model to use (default: gpt-4)')
    
    args = parser.parse_args()
    
    print("AI Log Explainer - Starting analysis...")
    print(f"Log file: {args.log_file}")
    print(f"Model: {args.model}")
    print("=" * 60)
    
    process_logs(args.log_file)
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()
