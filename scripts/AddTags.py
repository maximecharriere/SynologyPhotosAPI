"""
AddTags.py - Batch tag application script for Synology Photos

This script automatically applies team-specific tags to all photos in corresponding team folders.
It uses the Synology Photos API to:
1. Authenticate with the Synology Photos system
2. Process each team's folder recursively
3. Apply the corresponding team tag to all photos in that folder
"""

from typing import Dict, List
from dotenv import load_dotenv
import os
import sys
from SynologyPhotoLib import authenticate, get_items, add_tag, get_tag, SynologyPhotoError

# Mapping of team names to their folder IDs in Synology Photos
team_folders_id: Dict[str, int] = {
    "U20F": 3048,
    "U18M-2": 3042,
    "U18M-1": 3037,
    "U16M-2": 3032,
    "U16M-1": 3027,
    "U16F": 3022,
    "U14M-2": 3017,
    "U14M-1": 3012,
    "U12-2": 3007,
    "U12-1": 3002,
    "U10-1": 2997,
    "3LRM": 2992,
    "3LRF": 2987,
    "2LRM": 2982,
    "1LNM": 2977
}

def process_team(sid: str, team_name: str, folder_id: int) -> None:
    """
    Process a single team's folder and apply team tags to all photos.

    Args:
        sid: Session ID from authentication
        team_name: Name of the team (used for tagging)
        folder_id: ID of the team's folder in Synology Photos

    Raises:
        SynologyPhotoError: If any API operation fails
    """
    try:
        print(f"Processing team {team_name}...")
        items = get_items(sid, folder_id, recursive=True)
        items_ids = [item['id'] for item in items]
        tag_id = get_tag(sid, team_name)['id']
        add_tag(sid, items_ids, [tag_id])
    except SynologyPhotoError as e:
        print(f"Error processing team {team_name}: {str(e)}", file=sys.stderr)


if __name__ == "__main__":
    """Main execution function."""
    load_dotenv()
    
    # Validate environment variables
    required_env = ['SYNOLOGY_PHOTO_USERNAME', 'SYNOLOGY_PHOTO_PASSWORD', 'SYNOLOGY_PHOTO_URL']
    missing_env = [var for var in required_env if not os.getenv(var)]
    if missing_env:
        print(f"Missing required environment variables: {', '.join(missing_env)}", file=sys.stderr)
        sys.exit(1)

    try:
        sid = authenticate(
            os.getenv('SYNOLOGY_PHOTO_USERNAME'),
            os.getenv('SYNOLOGY_PHOTO_PASSWORD')
        )
        
        print(f"Processing {len(team_folders_id)} teams...")
        for team_name, folder_id in team_folders_id.items():
            process_team(sid, team_name, folder_id)
            
        print("All teams processed successfully")
    except SynologyPhotoError as e:
        print(f"Fatal error: {str(e)}", file=sys.stderr)
        sys.exit(1)
