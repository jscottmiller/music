#!/usr/bin/env python3
"""Scan a digital music directory and generate XML catalog."""

import os
import re
import sys
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def parse_folder_name(name):
    """Try to extract artist and album from folder name."""
    # Common patterns:
    # "Artist - Album"
    # "Artist - Album (extra info)"
    # "Album Name (gamerip)"

    # Skip non-music files
    if name.endswith(('.py', '.bat', '.exe', '.txt')):
        return None

    # Check for "Artist - Album" pattern
    if ' - ' in name:
        parts = name.split(' - ', 1)
        artist = parts[0].strip()
        album = parts[1].strip()
        return {'artist': artist, 'album': album}

    # Probably a soundtrack or compilation
    return {'artist': 'Various', 'album': name}

def get_format(path):
    """Detect the audio format in a directory."""
    formats = set()
    try:
        for f in os.listdir(path):
            if f.lower().endswith('.flac'):
                formats.add('FLAC')
            elif f.lower().endswith('.mp3'):
                formats.add('MP3')
            elif f.lower().endswith('.wav'):
                formats.add('WAV')
            elif f.lower().endswith('.m4a'):
                formats.add('M4A')
            elif f.lower().endswith('.ogg'):
                formats.add('OGG')
    except PermissionError:
        pass

    if formats:
        return '/'.join(sorted(formats))
    return 'Unknown'

def scan_directory(music_dir):
    """Scan music directory and return album data."""
    albums = []

    for item in sorted(os.listdir(music_dir)):
        item_path = os.path.join(music_dir, item)
        if not os.path.isdir(item_path):
            continue

        parsed = parse_folder_name(item)
        if not parsed:
            continue

        fmt = get_format(item_path)

        albums.append({
            'artist': parsed['artist'],
            'album': parsed['album'],
            'format': fmt,
            'path': item_path
        })

    return albums

def generate_xml(albums):
    """Generate XML from album data."""
    root = Element('collection')
    root.set('type', 'digital')
    root.set('source', '/mnt/d/Music')

    # Group by artist
    by_artist = {}
    for album in albums:
        artist = album['artist']
        if artist not in by_artist:
            by_artist[artist] = []
        by_artist[artist].append(album)

    for artist in sorted(by_artist.keys()):
        for album in sorted(by_artist[artist], key=lambda x: x['album']):
            album_el = SubElement(root, 'album')
            album_el.set('artist', album['artist'])
            album_el.set('title', album['album'])

            fmt_el = SubElement(album_el, 'format')
            fmt_el.text = album['format']

            path_el = SubElement(album_el, 'path')
            path_el.text = album['path']

    # Pretty print
    rough_string = tostring(root, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='  ')

def main():
    music_dir = sys.argv[1] if len(sys.argv) > 1 else '/mnt/d/Music'

    print(f"Scanning {music_dir}...", file=sys.stderr)
    albums = scan_directory(music_dir)
    print(f"Found {len(albums)} albums", file=sys.stderr)

    xml = generate_xml(albums)
    # Remove the XML declaration line since we'll add our own
    lines = xml.split('\n')[1:]
    print('<?xml version="1.0" encoding="UTF-8"?>')
    print('<!--')
    print('  Digital music collection')
    print('  Auto-generated from /mnt/d/Music')
    print('-->')
    print('\n'.join(lines))

if __name__ == '__main__':
    main()
