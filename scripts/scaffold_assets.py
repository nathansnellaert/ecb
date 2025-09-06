#!/usr/bin/env python3
"""Scaffold all ECB dataset assets based on name mapping"""
import csv
from pathlib import Path
from typing import Dict, List

# Template for each dataset asset  
ASSET_TEMPLATE = '''from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("{dataflow_id}")
    
    if data.num_rows > 0:
        upload_data(data, "{friendly_name}")
        print(f"Uploaded {{data.num_rows}} rows to {friendly_name}")
        
    save_state("{friendly_name}", {{
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    }})
    
    return data
'''

def load_mapping() -> List[Dict[str, str]]:
    """Load the dataset name mapping from CSV"""
    mapping_file = Path(__file__).parent.parent / "defs" / "dataset_name_mapping.csv"
    mapping = []
    
    with open(mapping_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mapping.append(row)
    
    return mapping

def create_asset_file(dataset_info: Dict[str, str]) -> Path:
    """Create a single asset file for a dataset"""
    friendly_name = dataset_info['friendly_name']
    
    # Create asset directory
    asset_dir = Path(__file__).parent.parent / "assets" / friendly_name
    asset_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate asset code
    code = ASSET_TEMPLATE.format(
        friendly_name=friendly_name,
        dataflow_id=dataset_info['dataflow_id'],
        original_name=dataset_info.get('original_name', dataset_info['dataflow_id'])
    )
    
    # Write main.py in asset directory
    asset_file = asset_dir / "main.py"
    with open(asset_file, 'w') as f:
        f.write(code)
    
    return asset_file


def main():
    """Generate all dataset assets"""
    print("Loading dataset name mapping...")
    mapping = load_mapping()
    print(f"Found {len(mapping)} datasets")
    
    # Ask for confirmation
    response = input(f"\nThis will create {len(mapping)} asset directories. Continue? (y/n): ")
    if response.lower() != 'y':
        print("Aborted.")
        return
    
    # Create asset files
    print("\nGenerating asset files...")
    created_files = []
    for i, dataset in enumerate(mapping):
        if i % 10 == 0:
            print(f"Progress: {i}/{len(mapping)}")
        
        asset_file = create_asset_file(dataset)
        created_files.append(asset_file)
    
    print(f"\n✓ Created {len(created_files)} asset files")
    
    print("\n🎉 Scaffold complete!")
    print(f"Generated {len(mapping)} dataset assets in assets/")

if __name__ == "__main__":
    main()