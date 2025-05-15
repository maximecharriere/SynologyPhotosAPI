"""
UpdateTagsList.py - Synology Photos Tag Extractor

This script retrieves and saves all tag information from a Synology Photos installation.
The output is saved as a JSON file in the 'output' directory, making it useful for:
- Reviewing available tags in your Synology Photos system
- Getting tag IDs for use in other scripts
- Backup of tag information
"""

from dotenv import load_dotenv
import os
import json
import sys
from SynologyPhotoLib import authenticate, get_all_tags

load_dotenv()

# Create output directory if not exists
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
os.makedirs(output_dir, exist_ok=True)

try:
    sid = authenticate(
        os.getenv('SYNOLOGY_PHOTO_USERNAME'),
        os.getenv('SYNOLOGY_PHOTO_PASSWORD')
    )

    tags_info = get_all_tags(sid)

    output_file = os.path.join(output_dir, 'tags_info.json')
    with open(output_file, 'w') as f:
        json.dump(tags_info, f, indent=4)
        print(f"Tags info saved to {output_file}")
except Exception as e:
    print(f"Error: {str(e)}", file=sys.stderr)
    sys.exit(1)