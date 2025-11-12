"""
Airborne Track Binary File Extractor
Reads binary track files and converts to readable formats
"""
import struct
import json
import csv
from datetime import datetime
from pathlib import Path


class TrackExtractor:
    """Extract airborne track data from binary files"""
    
    MAGIC_NUMBER = b'ATRK'
    
    def __init__(self):
        self.tracks = []
        self.version = None
    
    def read_binary(self, filename):
        """Read tracks from binary file
        
        Returns:
            dict: Dictionary containing version and tracks data
        """
        self.tracks = []
        
        with open(filename, 'rb') as f:
            # Read and verify header
            magic = f.read(4)
            if magic != self.MAGIC_NUMBER:
                raise ValueError(f"Invalid file format. Expected {self.MAGIC_NUMBER}, got {magic}")
            
            self.version = struct.unpack('I', f.read(4))[0]
            num_tracks = struct.unpack('I', f.read(4))[0]
            
            print(f"Reading binary file: {filename}")
            print(f"Format version: {self.version}")
            print(f"Number of tracks: {num_tracks}")
            
            # Read each track
            for _ in range(num_tracks):
                track = self._read_track(f)
                self.tracks.append(track)
                print(f"  - Loaded: {track['track_name']} ({track['track_type']})")
        
        return {
            'version': str(self.version),
            'tracks': self.tracks
        }
    
    def _read_track(self, f):
        """Read a single track from the binary file"""
        # Read track ID
        track_id = struct.unpack('I', f.read(4))[0]
        
        # Read track name
        name_len = struct.unpack('I', f.read(4))[0]
        track_name = f.read(name_len).decode('utf-8')
        
        # Read track type
        type_len = struct.unpack('I', f.read(4))[0]
        track_type = f.read(type_len).decode('utf-8')
        
        # Read aircraft type
        aircraft_len = struct.unpack('I', f.read(4))[0]
        aircraft_type = f.read(aircraft_len).decode('utf-8')
        
        # Read time information
        start_time = struct.unpack('d', f.read(8))[0]
        end_time = struct.unpack('d', f.read(8))[0]
        lifetime = struct.unpack('d', f.read(8))[0]
        
        # Read positions
        num_positions = struct.unpack('I', f.read(4))[0]
        positions = []
        
        for _ in range(num_positions):
            position = {
                'timestamp': struct.unpack('d', f.read(8))[0],
                'range': struct.unpack('d', f.read(8))[0],
                'azimuth': struct.unpack('d', f.read(8))[0],
                'elevation': struct.unpack('d', f.read(8))[0],
                'speed': struct.unpack('d', f.read(8))[0],
                'heading': struct.unpack('d', f.read(8))[0]
            }
            positions.append(position)
        
        return {
            'track_id': track_id,
            'track_name': track_name,
            'track_type': track_type,
            'aircraft_type': aircraft_type,
            'start_time': start_time,
            'end_time': end_time,
            'lifetime': lifetime,
            'positions': positions
        }
    
    def export_to_json(self, output_filename):
        """Export tracks to JSON format"""
        data = {
            'version': str(self.version),
            'tracks': self.tracks
        }
        
        with open(output_filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nExported to JSON: {output_filename}")
        return output_filename
    
    def export_to_csv(self, output_filename):
        """Export tracks to CSV format (flattened positions)"""
        with open(output_filename, 'w', newline='') as f:
            fieldnames = [
                'track_id', 'track_name', 'track_type', 'aircraft_type',
                'track_start_time', 'track_end_time', 'lifetime',
                'timestamp', 'range', 'azimuth', 'elevation', 'speed', 'heading'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for track in self.tracks:
                for pos in track['positions']:
                    row = {
                        'track_id': track['track_id'],
                        'track_name': track['track_name'],
                        'track_type': track['track_type'],
                        'aircraft_type': track['aircraft_type'],
                        'track_start_time': datetime.fromtimestamp(track['start_time']).isoformat(),
                        'track_end_time': datetime.fromtimestamp(track['end_time']).isoformat(),
                        'lifetime': track['lifetime'],
                        'timestamp': datetime.fromtimestamp(pos['timestamp']).isoformat(),
                        'range': pos['range'],
                        'azimuth': pos['azimuth'],
                        'elevation': pos['elevation'],
                        'speed': pos['speed'],
                        'heading': pos['heading']
                    }
                    writer.writerow(row)
        
        print(f"Exported to CSV: {output_filename}")
        return output_filename
    
    def export_summary(self, output_filename):
        """Export a human-readable summary of tracks"""
        with open(output_filename, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("AIRBORNE TRACK DATA SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Format Version: {self.version}\n")
            f.write(f"Total Tracks: {len(self.tracks)}\n\n")
            
            for i, track in enumerate(self.tracks, 1):
                f.write("-" * 80 + "\n")
                f.write(f"Track #{i}\n")
                f.write("-" * 80 + "\n")
                f.write(f"ID:           {track['track_id']}\n")
                f.write(f"Name:         {track['track_name']}\n")
                f.write(f"Type:         {track['track_type'].upper()}\n")
                f.write(f"Aircraft:     {track['aircraft_type']}\n")
                f.write(f"Start Time:   {datetime.fromtimestamp(track['start_time']).strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"End Time:     {datetime.fromtimestamp(track['end_time']).strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Lifetime:     {track['lifetime'] / 60:.1f} minutes ({track['lifetime']:.0f} seconds)\n")
                f.write(f"Data Points:  {len(track['positions'])}\n\n")
                
                if track['positions']:
                    first_pos = track['positions'][0]
                    last_pos = track['positions'][-1]
                    
                    f.write("First Position:\n")
                    f.write(f"  Time:      {datetime.fromtimestamp(first_pos['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"  Range:     {first_pos['range']:.2f} NM\n")
                    f.write(f"  Azimuth:   {first_pos['azimuth']:.1f}°\n")
                    f.write(f"  Elevation: {first_pos['elevation']:.0f} ft\n")
                    f.write(f"  Speed:     {first_pos['speed']:.0f} knots\n")
                    f.write(f"  Heading:   {first_pos['heading']:.1f}°\n\n")
                    
                    f.write("Last Position:\n")
                    f.write(f"  Time:      {datetime.fromtimestamp(last_pos['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"  Range:     {last_pos['range']:.2f} NM\n")
                    f.write(f"  Azimuth:   {last_pos['azimuth']:.1f}°\n")
                    f.write(f"  Elevation: {last_pos['elevation']:.0f} ft\n")
                    f.write(f"  Speed:     {last_pos['speed']:.0f} knots\n")
                    f.write(f"  Heading:   {last_pos['heading']:.1f}°\n\n")
        
        print(f"Exported summary: {output_filename}")
        return output_filename
    
    def get_tracks(self):
        """Return the loaded tracks"""
        return self.tracks


def main():
    """Demo extraction from binary file"""
    extractor = TrackExtractor()
    
    # Check if binary file exists
    binary_file = 'airborne_tracks.bin'
    if not Path(binary_file).exists():
        print(f"Error: {binary_file} not found!")
        print("Please run track_generator.py first to create the binary file.")
        return
    
    # Read binary file
    data = extractor.read_binary(binary_file)
    
    # Export to various formats
    print("\nExporting to readable formats...")
    extractor.export_to_json('airborne_tracks_extracted.json')
    extractor.export_to_csv('airborne_tracks_extracted.csv')
    extractor.export_summary('airborne_tracks_summary.txt')
    
    print("\n" + "=" * 80)
    print("Extraction complete!")
    print("=" * 80)


if __name__ == '__main__':
    main()
