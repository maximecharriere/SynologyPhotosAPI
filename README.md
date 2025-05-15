# Synology Photos API Client

A Python client library and utility scripts for interacting with the Synology Photos API.

## Project Overview

This project provides tools to interact with Synology Photos through its unofficial API, allowing you to:
- Authenticate with your Synology Photos instance
- Browse folders and photos
- Get information about tags
- Apply tags to photos automatically
- Extract API information for reference

## Installation

1. Clone this repository
2. Install dependencies: `pip install requests python-dotenv`

## Setup
Create a `.env` with these variables:
  - `SYNOLOGY_PHOTO_USERNAME`: Synology account username
  - `SYNOLOGY_PHOTO_PASSWORD`: Synology account password
  - `SYNOLOGY_PHOTO_URL`: Base URL of the Synology Photos installation

## Available Scripts

- `scripts/AddTags.py`: Automatically applies team tags to photos in their respective folders
- `scripts/UpdateTagsList.py`: Retrieves and saves all available tags from your Synology Photos
- `scripts/UpdateApiInfo.py`: Extracts API reference information

## Resources
- SynologyPhotosAPI Unofficial Doc 1: https://github.com/zeichensatz/SynologyPhotosAPI
- SynologyPhotosAPI Unofficial Doc 2: https://blog.jbowen.dev/synology/photostation/
