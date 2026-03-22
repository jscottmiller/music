# Music Database

Personal music interests and collection tracking using ad hoc XML.

## Structure

```
data/           # General music interests (artists, genres, notes)
collections/    # Physical and digital collection catalogs
  digital.xml   # Digital library (auto-generated from D:\Music)
  vinyl.xml     # Vinyl collection (manual entries)
tools/          # Scripts for managing the database
```

## XML Conventions

No strict schema - XML structure is intentionally flexible. Common patterns:

- `<album artist="..." title="...">` for albums
- `<artist name="...">` for artist entries
- `<note>` for freeform thoughts
- Nest whatever attributes/elements make sense for the data

## Tools

- `tools/scan_digital.py [path]` - Scan a directory and generate collection XML
  - Defaults to `/mnt/d/Music` (Windows host music folder via WSL)
  - Parses "Artist - Album" folder naming convention
  - Detects audio formats (FLAC, MP3, etc.)

## Collection Tracking

**Digital**: Auto-scanned from local files. Format info included.

**Vinyl**: Manual entries with optional Discogs-style metadata:
- Pressing info (label, catalog #, country, variant)
- Condition grades (VG, VG+, NM, M)
- Acquisition details (date, source, price)
