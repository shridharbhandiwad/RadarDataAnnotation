# Airborne Track Data Processing and Visualization

A comprehensive Python application for processing, analyzing, and visualizing airborne track data. This system includes binary file generation, extraction, format conversion, and an interactive GUI with drag-and-drop functionality.

## Features

### 🔧 Core Functionality
- **Binary Track File Format**: Custom binary format for efficient storage of airborne track data
- **Track Data Generation**: Create sample tracks with realistic flight patterns (incoming/outgoing)
- **Data Extraction**: Read and parse binary track files
- **Format Conversion**: Export to JSON, CSV, and human-readable summary formats

### 🖥️ Interactive GUI
- **Drag & Drop Interface**: Simply drag binary files into the application
- **File Browser**: Traditional file selection dialog
- **Track Selection**: Click to select and highlight individual tracks
- **Trajectory Visualization**: Interactive plots showing flight paths
- **Track Details Panel**: Comprehensive information about selected tracks
- **Export Functions**: Export data in multiple formats directly from the GUI

### 📊 Visualization
- **Multi-track Display**: View all tracks simultaneously
- **Selective Highlighting**: Focus on individual tracks while showing others in context
- **Direction Indicators**: Arrows showing flight direction
- **Start/End Markers**: Clear visual indicators for track endpoints
- **Interactive Controls**: Zoom, pan, and explore trajectories

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. **Clone or download the project**
   ```bash
   cd /workspace
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   The project requires:
   - `matplotlib` - For plotting and visualization
   - `tkinterdnd2` - For drag-and-drop functionality

## Usage

### 1. Generate Sample Binary File

First, create a sample binary file with two tracks (one incoming, one outgoing):

```bash
python3 track_generator.py
```

This will create:
- `airborne_tracks.bin` - Binary file containing track data
- `airborne_tracks_reference.json` - JSON reference for verification

**Output:**
```
Binary file saved to: airborne_tracks.bin
Number of tracks: 2
  - INC-ALPHA-001 (incoming): 60 positions
  - OUT-BRAVO-002 (outgoing): 80 positions

Reference JSON saved to: airborne_tracks_reference.json
```

### 2. Extract and Convert (Command Line)

Extract data from binary file and convert to readable formats:

```bash
python3 track_extractor.py
```

This will create:
- `airborne_tracks_extracted.json` - JSON format
- `airborne_tracks_extracted.csv` - CSV format (flattened)
- `airborne_tracks_summary.txt` - Human-readable summary

### 3. Launch GUI Application

Start the interactive viewer:

```bash
python3 track_viewer_gui.py
```

Or use the convenient launcher script:

```bash
./run_gui.sh
```

**GUI Features:**

1. **Load Files**:
   - Drag and drop a `.bin` file onto the drop zone, OR
   - Click "Browse File..." to select a file

2. **View Tracks**:
   - All tracks are displayed on the map
   - Different colors for incoming (blue) and outgoing (magenta) tracks
   - Circle markers indicate start positions
   - Square markers indicate end positions

3. **Select Track**:
   - Click on a track in the list
   - The selected track is highlighted on the map
   - Detailed information appears in the details panel
   - Direction arrows show flight path

4. **Export Data**:
   - Click "Export to JSON" for JSON format
   - Click "Export to CSV" for spreadsheet format
   - Click "Export Summary" for text summary

## Data Structure

### Track Object

Each track contains the following information:

```json
{
  "track_id": 1001,
  "track_name": "INC-ALPHA-001",
  "track_type": "incoming",
  "aircraft_type": "Boeing 737",
  "start_time": 1699564800.0,
  "end_time": 1699566600.0,
  "lifetime": 1800.0,
  "positions": [
    {
      "timestamp": 1699564800.0,
      "latitude": 40.0,
      "longitude": -75.0,
      "altitude": 35000.0,
      "speed": 450.0,
      "heading": 270.0
    }
  ]
}
```

### Binary Format Specification

The binary file format is structured as follows:

```
Header:
- Magic number (4 bytes): 'ATRK'
- Version (4 bytes): uint32
- Number of tracks (4 bytes): uint32

For each track:
- track_id (4 bytes): uint32
- track_name_len (4 bytes): uint32
- track_name (variable): UTF-8 string
- track_type_len (4 bytes): uint32
- track_type (variable): UTF-8 string
- aircraft_type_len (4 bytes): uint32
- aircraft_type (variable): UTF-8 string
- start_time (8 bytes): double
- end_time (8 bytes): double
- lifetime (8 bytes): double
- num_positions (4 bytes): uint32

For each position:
- timestamp (8 bytes): double
- latitude (8 bytes): double
- longitude (8 bytes): double
- altitude (8 bytes): double
- speed (8 bytes): double
- heading (8 bytes): double
```

## File Descriptions

### Core Files

- **`track_schema.json`**: JSON schema defining the track data structure
- **`track_generator.py`**: Generates sample binary track files
- **`track_extractor.py`**: Reads binary files and converts to readable formats
- **`track_viewer_gui.py`**: Interactive GUI application
- **`requirements.txt`**: Python package dependencies

### Generated Files

- **`airborne_tracks.bin`**: Binary track data file (generated)
- **`airborne_tracks_reference.json`**: JSON reference (generated)
- **`airborne_tracks_extracted.json`**: Extracted JSON (generated)
- **`airborne_tracks_extracted.csv`**: Extracted CSV (generated)
- **`airborne_tracks_summary.txt`**: Human-readable summary (generated)

## Examples

### Example Track: Incoming Flight

```
Track #1
--------------------------------------------------------------------------------
ID:           1001
Name:         INC-ALPHA-001
Type:         INCOMING
Aircraft:     Boeing 737
Start Time:   2025-11-10 10:00:00
End Time:     2025-11-10 10:30:00
Lifetime:     30.0 minutes (1800 seconds)
Data Points:  60

First Position:
  Time:      2025-11-10 10:00:00
  Location:  40.0000°N, -75.0000°E
  Altitude:  35000 ft
  Speed:     450 knots
  Heading:   270.0°

Last Position:
  Time:      2025-11-10 10:30:00
  Location:  39.8000°N, -75.5000°E
  Altitude:  1000 ft
  Speed:     225 knots
  Heading:   270.0°
```

## Track Types

### Incoming Tracks
- Aircraft approaching an airport
- Descending altitude profile
- Decelerating speed
- Example: INC-ALPHA-001

### Outgoing Tracks
- Aircraft departing from an airport
- Climbing altitude profile
- Accelerating speed
- Example: OUT-BRAVO-002

## Technical Details

### Data Validation
- Binary files are validated with magic number 'ATRK'
- Version checking ensures compatibility
- UTF-8 encoding for text fields

### Performance
- Efficient binary format reduces file size
- Streaming read/write for large datasets
- Optimized visualization rendering

### Extensibility
- Modular design for easy feature addition
- Clear separation between data layer and UI
- Schema-based structure allows version upgrades

## Troubleshooting

### Issue: "Invalid file format"
**Solution**: Ensure the file was generated by `track_generator.py` or follows the binary format specification.

### Issue: GUI doesn't start
**Solution**: Make sure `tkinterdnd2` is installed:
```bash
pip install tkinterdnd2
```

### Issue: Drag and drop doesn't work
**Solution**: 
- On Linux, you may need to install additional packages:
  ```bash
  sudo apt-get install python3-tk
  ```
- Try using the "Browse File..." button instead

### Issue: Visualization is slow
**Solution**: For large track files with many positions, the rendering may take time. Consider reducing the number of position points or increasing the interval between points.

## Future Enhancements

Potential features for future versions:
- [ ] 3D trajectory visualization with altitude
- [ ] Real-time track data streaming
- [ ] Track filtering by time, altitude, or speed
- [ ] Export to KML for Google Earth
- [ ] Animation playback of tracks
- [ ] Multiple file comparison
- [ ] Track statistics and analytics

## License

This project is provided as-is for educational and development purposes.

## Author

Created as part of an airborne track data processing system.

## Version History

- **v1.0** (2025-11-10): Initial release
  - Binary file format
  - Data generation and extraction
  - Interactive GUI with visualization
  - Multiple export formats
