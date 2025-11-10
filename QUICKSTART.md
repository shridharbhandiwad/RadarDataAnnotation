# Quick Start Guide

Get started with the Airborne Track Viewer in 3 simple steps!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `matplotlib` - For visualization
- `tkinterdnd2` - For drag-and-drop support

## Step 2: Generate Sample Data

```bash
python3 track_generator.py
```

This creates `airborne_tracks.bin` with two sample tracks:
- **INC-ALPHA-001**: Incoming Boeing 737 (30 minutes, 60 data points)
- **OUT-BRAVO-002**: Outgoing Airbus A320 (40 minutes, 80 data points)

## Step 3: Launch the GUI

```bash
python3 track_viewer_gui.py
```

Or use the launcher:

```bash
./run_gui.sh
```

## Using the GUI

### Load a File
1. **Drag & Drop**: Drag `airborne_tracks.bin` onto the drop zone
2. **Browse**: Click "Browse File..." and select the file

### View Tracks
- All tracks appear on the map automatically
- 🛬 Blue = Incoming tracks
- 🛫 Magenta = Outgoing tracks
- ⚪ Circle = Start position
- ⬜ Square = End position

### Select a Track
1. Click on a track name in the list
2. The track is highlighted on the map
3. Details appear in the right panel
4. Direction arrows show flight path

### Export Data
- **JSON**: Full data structure
- **CSV**: Spreadsheet format
- **Summary**: Human-readable text

## Command Line Tools

### Extract Data Without GUI

```bash
python3 track_extractor.py
```

Outputs:
- `airborne_tracks_extracted.json`
- `airborne_tracks_extracted.csv`
- `airborne_tracks_summary.txt`

### View Summary

```bash
cat airborne_tracks_summary.txt
```

## Troubleshooting

### Drag & Drop Not Working?
Use the "Browse File..." button instead.

### Missing Dependencies?
```bash
pip install matplotlib tkinterdnd2
```

### Python Not Found?
Make sure Python 3.7+ is installed:
```bash
python3 --version
```

## What's Next?

- Check out `README.md` for detailed documentation
- Explore the JSON schema in `track_schema.json`
- Examine the binary format specification
- Create your own track data

## Sample Output

When you load the sample file, you'll see:

```
Track #1: INC-ALPHA-001 (INCOMING)
- Boeing 737
- 30 minutes flight time
- Descending from 35,000 ft to 1,000 ft
- Decelerating from 450 to 225 knots

Track #2: OUT-BRAVO-002 (OUTGOING)
- Airbus A320
- 40 minutes flight time
- Climbing from 1,000 ft to 35,000 ft
- Accelerating from 150 to 500 knots
```

Enjoy exploring airborne tracks! 🛫✈️🛬
