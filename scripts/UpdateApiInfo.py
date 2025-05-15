"""
UpdateApiInfo.py - Synology Photos API Reference Extractor

This script retrieves and saves the complete API reference information from
a Synology Photos installation. The output is saved as a JSON file in the
'output' directory and can be used for:
- Exploring available API endpoints
- Documentation purposes
- Understanding API structure and options
"""

from dotenv import load_dotenv
import json
import os
import sys
from SynologyPhotoLib import get_api_info

load_dotenv()

# Create output directory if not exists
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
os.makedirs(output_dir, exist_ok=True)

try:
    data = get_api_info()

    output_file = os.path.join(output_dir, 'api_info.json')
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
        print(f"API info saved to {output_file}")
except Exception as e:
    print(f"Error: {str(e)}", file=sys.stderr)
    sys.exit(1)