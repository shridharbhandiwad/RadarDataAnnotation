"""
Airborne Track Binary File Generator
Creates binary files containing airborne track data
"""
import struct
import json
import time
import math
from datetime import datetime, timedelta

class TrackGenerator:
    """Generate sample airborne tracks and save to binary format"""
    
    # Binary format specification
    MAGIC_NUMBER = b'ATRK'  # File signature
    VERSION = 1
    
    def __init__(self):
        self.tracks = []
    
    def generate_sample_tracks(self):
        """Generate two sample tracks: one incoming, one outgoing"""
        current_time = time.time()
        
        # Track 1: Incoming flight (approaching from east)
        incoming_track = {
            'track_id': 1001,
            'track_name': 'INC-ALPHA-001',
            'track_type': 'incoming',
            'aircraft_type': 'Boeing 737',
            'start_time': current_time - 1800,  # Started 30 minutes ago
            'end_time': current_time,
            'lifetime': 1800,  # 30 minutes
            'positions': self._generate_incoming_positions(current_time)
        }
        
        # Track 2: Outgoing flight (departing to west)
        outgoing_track = {
            'track_id': 2001,
            'track_name': 'OUT-BRAVO-002',
            'track_type': 'outgoing',
            'aircraft_type': 'Airbus A320',
            'start_time': current_time - 2400,  # Started 40 minutes ago
            'end_time': current_time,
            'lifetime': 2400,  # 40 minutes
            'positions': self._generate_outgoing_positions(current_time)
        }
        
        self.tracks = [incoming_track, outgoing_track]
        return self.tracks
    
    def _generate_incoming_positions(self, end_time):
        """Generate position data for incoming track"""
        positions = []
        num_points = 60  # One point per 30 seconds
        start_range = 150.0  # Starting range in nautical miles
        end_range = 5.0  # Final range (close to radar)
        start_azimuth = 90.0  # Starting azimuth (east)
        end_azimuth = 270.0  # Final azimuth (west)
        
        for i in range(num_points):
            progress = i / (num_points - 1)
            timestamp = end_time - 1800 + (i * 30)
            
            # Calculate range (approaching)
            range_val = start_range + (end_range - start_range) * progress
            
            # Calculate azimuth (sweeping from east to west)
            azimuth = start_azimuth + (end_azimuth - start_azimuth) * progress
            
            # Calculate elevation (descending approach)
            elevation = 35000 * (1 - progress) + 1000 * progress
            
            # Calculate speed (decelerating)
            speed = 450 * (1 - progress * 0.5)  # From 450 to 225 knots
            
            # Calculate heading (towards airport)
            heading = 270 + math.sin(progress * math.pi) * 10
            
            positions.append({
                'timestamp': timestamp,
                'range': range_val,
                'azimuth': azimuth,
                'elevation': elevation,
                'speed': speed,
                'heading': heading
            })
        
        return positions
    
    def _generate_outgoing_positions(self, end_time):
        """Generate position data for outgoing track"""
        positions = []
        num_points = 80  # One point per 30 seconds
        start_range = 3.0  # Starting range (near radar)
        end_range = 180.0  # Final range in nautical miles
        start_azimuth = 240.0  # Starting azimuth (southwest)
        end_azimuth = 320.0  # Final azimuth (northwest)
        
        for i in range(num_points):
            progress = i / (num_points - 1)
            timestamp = end_time - 2400 + (i * 30)
            
            # Calculate range (departing)
            range_val = start_range + (end_range - start_range) * progress
            
            # Calculate azimuth (sweeping from southwest to northwest)
            azimuth = start_azimuth + (end_azimuth - start_azimuth) * progress
            
            # Calculate elevation (climbing departure)
            elevation = 1000 + 34000 * progress
            
            # Calculate speed (accelerating)
            speed = 150 + 350 * progress  # From 150 to 500 knots
            
            # Calculate heading (away from airport)
            heading = 250 - math.sin(progress * math.pi) * 15
            
            positions.append({
                'timestamp': timestamp,
                'range': range_val,
                'azimuth': azimuth,
                'elevation': elevation,
                'speed': speed,
                'heading': heading
            })
        
        return positions
    
    def save_to_binary(self, filename):
        """Save tracks to binary file
        
        Binary format:
        - Magic number (4 bytes): 'ATRK'
        - Version (4 bytes): uint32
        - Number of tracks (4 bytes): uint32
        - For each track:
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
            - For each position:
                - timestamp (8 bytes): double
                - range (8 bytes): double
                - azimuth (8 bytes): double
                - elevation (8 bytes): double
                - speed (8 bytes): double
                - heading (8 bytes): double
        """
        with open(filename, 'wb') as f:
            # Write header
            f.write(self.MAGIC_NUMBER)
            f.write(struct.pack('I', self.VERSION))
            f.write(struct.pack('I', len(self.tracks)))
            
            # Write each track
            for track in self.tracks:
                # Track metadata
                f.write(struct.pack('I', track['track_id']))
                
                # Track name
                name_bytes = track['track_name'].encode('utf-8')
                f.write(struct.pack('I', len(name_bytes)))
                f.write(name_bytes)
                
                # Track type
                type_bytes = track['track_type'].encode('utf-8')
                f.write(struct.pack('I', len(type_bytes)))
                f.write(type_bytes)
                
                # Aircraft type
                aircraft_bytes = track['aircraft_type'].encode('utf-8')
                f.write(struct.pack('I', len(aircraft_bytes)))
                f.write(aircraft_bytes)
                
                # Time information
                f.write(struct.pack('d', track['start_time']))
                f.write(struct.pack('d', track['end_time']))
                f.write(struct.pack('d', track['lifetime']))
                
                # Positions
                f.write(struct.pack('I', len(track['positions'])))
                for pos in track['positions']:
                    f.write(struct.pack('d', pos['timestamp']))
                    f.write(struct.pack('d', pos['range']))
                    f.write(struct.pack('d', pos['azimuth']))
                    f.write(struct.pack('d', pos['elevation']))
                    f.write(struct.pack('d', pos['speed']))
                    f.write(struct.pack('d', pos['heading']))
        
        import sys
        print(f"✓ Binary file saved to: {filename}")
        print(f"  File size: {self._get_file_size(filename)}")
        print(f"  Number of tracks: {len(self.tracks)}")
        sys.stdout.flush()
    
    def _get_file_size(self, filename):
        """Get human-readable file size"""
        import os
        size = os.path.getsize(filename)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"


def main():
    """Generate sample binary file"""
    import sys
    
    print("="*80)
    print("AIRBORNE TRACK GENERATOR")
    print("="*80)
    print("\n[1/3] Generating sample tracks...")
    sys.stdout.flush()
    
    generator = TrackGenerator()
    tracks = generator.generate_sample_tracks()
    print(f"✓ Generated {len(tracks)} tracks successfully")
    for track in tracks:
        print(f"  - {track['track_name']} ({track['track_type']}): {len(track['positions'])} positions")
    sys.stdout.flush()
    
    print("\n[2/3] Saving binary file...")
    sys.stdout.flush()
    generator.save_to_binary('airborne_tracks.bin')
    sys.stdout.flush()
    
    # Also save as JSON for reference
    print("\n[3/3] Saving JSON reference...")
    sys.stdout.flush()
    with open('airborne_tracks_reference.json', 'w') as f:
        json.dump({
            'version': '1.0',
            'tracks': generator.tracks
        }, f, indent=2)
    print("✓ Reference JSON saved to: airborne_tracks_reference.json")
    
    print("\n" + "="*80)
    print("✓ GENERATION COMPLETE!")
    print("="*80)
    print("\nGenerated files:")
    print("  1. airborne_tracks.bin - Binary track data")
    print("  2. airborne_tracks_reference.json - JSON reference")
    print("\nNext steps:")
    print("  - Run 'python3 track_extractor.py' to extract data")
    print("  - Run 'python3 track_viewer_gui.py' to view in GUI")
    print("="*80 + "\n")
    sys.stdout.flush()


if __name__ == '__main__':
    main()
