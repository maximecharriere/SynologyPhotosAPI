"""
SynologyPhotoLib.py - Synology Photos API Client Library

This library provides functions to interact with the Synology Photos API,
allowing you to browse folders, retrieve photos and videos, manage tags,
and perform other common operations with Synology Photos.

Functions:
- authenticate - Get session ID for API access
- get_api_info - Retrieve API documentation
- get_folders - List folders in Synology Photos
- get_items - Retrieve photos and videos from folders
- get_all_tags - Retrieve all tags from Synology Photos
- get_tag - Get information about a specific tag
- add_tag - Apply tags to photos or videos

"""

from typing import List, Dict, Optional, Any
import json
import os
from urllib.parse import urljoin
import requests

class SynologyPhotoError(Exception):
    """Custom exception for Synology Photo API errors."""
    pass

def authenticate(username: str, password: str) -> str:
    """Authenticate with the Synology Photo API.

    Args:
        username: The Synology account username.
        password: The Synology account password.

    Returns:
        str: The session ID (sid) for authenticated requests.

    Raises:
        SynologyPhotoError: If authentication fails or request fails.
    """
    endpoint = urljoin(os.getenv('SYNOLOGY_PHOTO_URL'), 'webapi/auth.cgi')
    params = {
        'api': 'SYNO.API.Auth',
        'version': 7,
        'method': 'login',
        'account': username,
        'passwd': password
    }
    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        raise SynologyPhotoError(f"Request failed: {response.status_code}")

    data = response.json()
    if not data['success']:
        raise SynologyPhotoError(f"Authentication failed: {data['error']['code']}")
    
    return data['data']['sid']

def get_api_info() -> Dict[str, Any]:
    """Retrieve API information from Synology Photo API.

    Returns:
        Dict[str, Any]: API information including available endpoints and versions.

    Raises:
        SynologyPhotoError: If the API request fails.
    """
    endpoint = urljoin(os.getenv('SYNOLOGY_PHOTO_URL'), 'webapi/query.cgi')
    params = {
        'api': 'SYNO.API.Info',
        'version': 1,
        'method': 'query'
    }
    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        raise SynologyPhotoError(f"Request failed: {response.status_code}")

    data = response.json()
    if not data['success']:
        raise SynologyPhotoError(f"Failed to get API Info: {data['error']['code']}")
    
    return data['data']

def get_folders(sid: str, folder_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Retrieve folders from Synology Photo.

    Args:
        sid: Session ID from authentication.
        folder_id: Optional ID of the parent folder. If None, returns root folders.

    Returns:
        List[Dict[str, Any]]: List of folder information dictionaries.

    Raises:
        SynologyPhotoError: If the folder request fails.
    """
    endpoint = urljoin(os.getenv('SYNOLOGY_PHOTO_URL'), 'webapi/entry.cgi')
    params = {
        'api': 'SYNO.Foto.Browse.Folder',
        'version': 2,
        'id': folder_id,
        'method': 'list',
        '_sid': sid,
        'offset': 0,
        'limit': 100,
    }
    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        raise SynologyPhotoError(f"Request failed: {response.status_code}")

    data = response.json()
    if not data['success']:
        raise SynologyPhotoError(f"Failed to get root folders: {data['error']['code']}")

    return data['data']['list']

def get_items(sid: str, folder_id: Optional[int] = None, recursive: bool = False) -> List[Dict[str, Any]]:
    """Retrieve items (photos/videos) from Synology Photo API.

    Args:
        sid: Session ID from authentication.
        folder_id: Optional ID of the folder to list items from.
        recursive: If True, retrieves items from all subfolders recursively.

    Returns:
        List[Dict[str, Any]]: List of item information dictionaries.

    Raises:
        SynologyPhotoError: If the items request fails.
    """
    endpoint = urljoin(os.getenv('SYNOLOGY_PHOTO_URL'), 'webapi/entry.cgi')
    params = {
        'api': 'SYNO.Foto.Browse.Item',
        'version': 4,
        'folder_id': folder_id,
        'method': 'list',
        '_sid': sid,
        'offset': 0,
        'limit': 100,
        'additional': '["tag"]'
    }
    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        raise SynologyPhotoError(f"Request failed: {response.status_code}")

    data = response.json()
    if not data['success']:
        raise SynologyPhotoError(f"Failed to get items: {data['error']['code']}")
    
    items = data['data']['list']
    
    if recursive:
        for folder in get_folders(sid, folder_id):
            items.extend(get_items(sid, folder['id'], recursive=True))
    
    return items

def get_all_tags(sid: str) -> List[Dict[str, Any]]:
    """Retrieve all tags from Synology Photo API.

    Args:
        sid: Session ID from authentication.

    Returns:
        List[Dict[str, Any]]: List of tag information dictionaries.

    Raises:
        SynologyPhotoError: If the tags request fails.
    """
    endpoint = urljoin(os.getenv('SYNOLOGY_PHOTO_URL'), 'webapi/entry.cgi')
    params = {
        'api': 'SYNO.Foto.Browse.GeneralTag',
        'version': 1,
        'method': 'list',
        '_sid': sid,  
        'limit': 100,
        'offset': 0,
    }
    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        raise SynologyPhotoError(f"Request failed: {response.status_code}")

    data = response.json()
    if not data['success']:
        raise SynologyPhotoError(f"Failed to get all tags: {data['error']['code']}")

    return data['data']['list']

def get_tag(sid: str, tag_name: str) -> Dict[str, Any]:
    """Retrieve a specific tag by name.

    Args:
        sid: Session ID from authentication.
        tag_name: Name of the tag to retrieve.

    Returns:
        Dict[str, Any]: Tag information dictionary.

    Raises:
        SynologyPhotoError: If the tag is not found or request fails.
    """
    tags = get_all_tags(sid)
    for tag in tags:
        if tag['name'] == tag_name:
            return tag
    raise SynologyPhotoError(f"Tag '{tag_name}' not found.")

def add_tag(sid: str, item_ids: List[int], tag_ids: List[int]) -> None:
    """Add tags to specified items.

    Args:
        sid: Session ID from authentication.
        item_ids: List of item IDs to tag.
        tag_ids: List of tag IDs to apply.

    Raises:
        SynologyPhotoError: If adding tags fails.
    """
    endpoint = urljoin(os.getenv('SYNOLOGY_PHOTO_URL'), 'webapi/entry.cgi')
    params = {
        'api': 'SYNO.Foto.Browse.Item',
        'version': 1,
        'method': 'add_tag',
        '_sid': sid,
        'id': json.dumps(item_ids),    
        'tag': json.dumps(tag_ids),    
    }

    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        raise SynologyPhotoError(f"Request failed: {response.status_code}")

    data = response.json()
    if not data['success']:
        raise SynologyPhotoError(f"Failed to add tags: {data['error']['code']}")