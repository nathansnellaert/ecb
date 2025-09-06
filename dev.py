"""Investigate why some connectors show verbose output"""
import os
import sys

# Set environment variables
os.environ['CONNECTOR_NAME'] = 'ecb'
os.environ['RUN_ID'] = 'test-output'
os.environ['ENABLE_HTTP_CACHE'] = 'true'
os.environ['STORAGE_BACKEND'] = 'local'
os.environ['DATA_DIR'] = 'data'

# Import after setting env vars
from assets.agricultural_statistics.main import main as agr_main
from assets.ameco_macroeconomic.main import main as ameco_main

print("=" * 80)
print("Investigating output differences between connectors")
print("=" * 80)

print("\n1. Testing agricultural_statistics connector:")
print("-" * 40)
# Capture what the agricultural_statistics main function does
agr_result = agr_main()
print(f"Result type: {type(agr_result)}")
print(f"Result: {agr_result}")

print("\n2. Testing ameco_macroeconomic connector:")
print("-" * 40)
# Check if the ameco connector has different output
try:
    ameco_result = ameco_main()
    print(f"Result type: {type(ameco_result)}")
    print(f"Result: {ameco_result}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 80)