#!/usr/bin/env python3
"""Generate friendly dataset names using Claude Code"""
import json
import csv
import os
import subprocess
from pathlib import Path

def get_dataflows():
    """Load dataflows from JSON file"""
    # Load from the defs directory
    dataflows_path = Path(__file__).parent.parent / "defs" / "dataflows.json"
    
    if not dataflows_path.exists():
        raise FileNotFoundError(f"Could not find dataflows.json. Run 'python scripts/fetch_dataflows.py' first to generate it.")
    
    with open(dataflows_path, 'r') as f:
        return json.load(f)

def create_batch_prompt(dataflows_batch):
    """Create prompt for Claude to generate names"""
    prompt = """Generate short, descriptive file/folder names for these ECB (European Central Bank) datasets. 

Rules:
- Use lowercase with underscores
- Keep names concise (between 3-5 words - should be unique)
- Make them descriptive and searchable
- Remove redundant words like "statistics", "data", "indicators"
- Use common abbreviations (gdp, cpi, eur, fx, etc.)
- Don't include years unless essential
- Remove "archived" and similar status words
- no special characters, only alphanumeric and underscores

These will be uploaded to a big data platform, so the names should be unique (preferably above 12 characters)

Return ONLY a JSON object with dataflow_id as key and friendly_name as value.

Datasets:
"""
    
    for df in dataflows_batch:
        prompt += f'\n{df["id"]}: "{df["name"]}"'
    
    prompt += "\n\nReturn ONLY the JSON mapping, no explanation."
    
    return prompt

def call_claude_code(prompt):
    """Call Claude Code CLI to generate names"""
    # Call Claude Code with the prompt directly
    result = subprocess.run(
        ["claude"],
        input=prompt,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise Exception(f"Claude Code failed: {result.stderr}")
    
    # Parse JSON from response
    response = result.stdout.strip()
    # Find JSON in response (between { and })
    start = response.find('{')
    end = response.rfind('}') + 1
    
    if start == -1 or end == 0:
        raise Exception(f"No JSON found in response: {response}")
    
    json_str = response[start:end]
    
    return json.loads(json_str)

def generate_mapping():
    """Generate dataset name mapping in batches"""
    dataflows = get_dataflows()
    print(f"Found {len(dataflows)} dataflows")
    
    # Output CSV file in defs directory
    csv_file = Path(__file__).parent.parent / "defs" / "dataset_name_mapping.csv"
    
    # Check if file exists to determine if we need headers
    file_exists = csv_file.exists()
    
    # Process in batches of 10
    batch_size = 10
    
    with open(csv_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['dataflow_id', 'original_name', 'friendly_name', 'description'])
        
        if not file_exists:
            writer.writeheader()
        
        for i in range(0, len(dataflows), batch_size):
            batch = dataflows[i:i + batch_size]
            print(f"\nProcessing batch {i//batch_size + 1} ({i+1}-{min(i+batch_size, len(dataflows))} of {len(dataflows)})")
            
            # Create prompt and get names from Claude
            prompt = create_batch_prompt(batch)
            name_mapping = call_claude_code(prompt)
            
            # Write to CSV
            for df in batch:
                friendly_name = name_mapping.get(df['id'], df['id'].lower())
                writer.writerow({
                    'dataflow_id': df['id'],
                    'original_name': df['name'],
                    'friendly_name': friendly_name,
                    'description': df.get('description', '')
                })
            
            # Force flush to disk after each batch
            f.flush()
            os.fsync(f.fileno())
            
            print(f"✓ Batch complete - wrote {len(batch)} entries")
                
    
    print(f"\nMapping saved to: {csv_file}")

if __name__ == "__main__":
    generate_mapping()