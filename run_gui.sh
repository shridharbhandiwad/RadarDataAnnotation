#!/bin/bash
# Launcher script for Airborne Track Viewer GUI

echo "=========================================="
echo "Airborne Track Viewer"
echo "=========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.7 or higher."
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
python3 -c "import matplotlib" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: matplotlib is not installed."
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

python3 -c "import tkinterdnd2" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Warning: tkinterdnd2 is not installed."
    echo "Drag-and-drop may not work."
    echo "Please run: pip install -r requirements.txt"
    echo ""
fi

# Check if sample binary file exists
if [ ! -f "airborne_tracks.bin" ]; then
    echo "Sample binary file not found. Generating..."
    python3 track_generator.py
    echo ""
fi

# Launch the GUI
echo "Launching GUI..."
python3 track_viewer_gui.py
