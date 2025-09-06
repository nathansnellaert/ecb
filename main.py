import os
os.environ['CONNECTOR_NAME'] = 'ecb'
os.environ['RUN_ID'] = os.getenv('RUN_ID', 'local-run')
from utils import validate_environment, upload_data, load_state
from pathlib import Path
import importlib.util
import sys
from datetime import datetime

def run_asset(asset_path: Path, asset_name: str):
    """Dynamically import and run an asset's main.py"""
    try:
        # Load the main.py module
        spec = importlib.util.spec_from_file_location(f"assets.{asset_name}.main", asset_path / "main.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[f"assets.{asset_name}.main"] = module
        spec.loader.exec_module(module)
        module.main()
        print(f"✓ {asset_name}: Completed successfully")

    except Exception as e:
        print(f"✗ {asset_name}: Failed - {e}")

def main():
    validate_environment()
    
    # Discover all asset directories with main.py
    assets_dir = Path(__file__).parent / "assets"
    asset_dirs = sorted([d for d in assets_dir.iterdir() if d.is_dir() and (d / "main.py").exists()])
    
    print(f"Found {len(asset_dirs)} total assets")
    
    # Pre-scan all assets to check their state
    completed_assets = []
    pending_assets = []
    
    for asset_dir in asset_dirs:
        asset_name = asset_dir.name
        state = load_state(asset_name)
        
        if state and 'last_updated' in state:
            last_updated = datetime.fromisoformat(state['last_updated'])
            days_ago = (datetime.now() - last_updated).days
            if days_ago < 30:
                completed_assets.append((asset_name, days_ago))
            else:
                pending_assets.append(asset_name)
        else:
            pending_assets.append(asset_name)
    
    # Print summary
    print(f"\n📊 Asset Status Summary:")
    print(f"  ✓ Completed (< 30 days): {len(completed_assets)}")
    print(f"  ⏳ Pending: {len(pending_assets)}")
    
    if completed_assets:
        print(f"\n✓ Recently completed assets ({len(completed_assets)}):")
        for name, days in sorted(completed_assets, key=lambda x: x[1])[:5]:
            print(f"  - {name} (updated {days} days ago)")
        if len(completed_assets) > 5:
            print(f"  ... and {len(completed_assets) - 5} more")
    
    if pending_assets:
        print(f"\n⏳ Assets to process ({len(pending_assets)}):")
        for name in pending_assets[:10]:
            print(f"  - {name}")
        if len(pending_assets) > 10:
            print(f"  ... and {len(pending_assets) - 10} more")
    
    # Process all pending assets
    if pending_assets:
        print(f"\n🚀 Starting processing of {len(pending_assets)} assets...")
        
        for i, asset_name in enumerate(pending_assets, 1):
            print(f"\n[{i}/{len(pending_assets)}] Processing {asset_name}...")
            asset_path = assets_dir / asset_name
            run_asset(asset_path, asset_name)
    else:
        print("\n✅ All assets are up to date!")
    
    print("\n✨ ECB connector run complete!")

if __name__ == "__main__":
    main()