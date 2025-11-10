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
        start_lat, start_lon = 40.0, -75.0  # Starting position (east)
        end_lat, end_lon = 39.8, -75.5  # Airport position
        
        for i in range(num_points):
            progress = i / (num_points - 1)
            timestamp = end_time - 1800 + (i * 30)
            
            # Interpolate position
            lat = start_lat + (end_lat - start_lat) * progress
            lon = start_lon + (end_lon - start_lon) * progress
            
            # Calculate altitude (descending approach)
            altitude = 35000 * (1 - progress) + 1000 * progress
            
            # Calculate speed (decelerating)
            speed = 450 * (1 - progress * 0.5)  # From 450 to 225 knots
            
            # Calculate heading (towards airport)
            heading = 270 + math.sin(progress * math.pi) * 10
            
            positions.append({
                'timestamp': timestamp,
                'latitude': lat,
                'longitude': lon,
                'altitude': altitude,
                'speed': speed,
                'heading': heading
            })
        
        return positions
    
    def _generate_outgoing_positions(self, end_time):
        """Generate position data for outgoing track"""
        positions = []
        num_points = 80  # One point per 30 seconds
        start_lat, start_lon = 39.8, -75.5  # Airport position
        end_lat, end_lon = 39.6, -76.5  # Destination (west)
        
        for i in range(num_points):
            progress = i / (num_points - 1)
            timestamp = end_time - 2400 + (i * 30)
            
            # Interpolate position
            lat = start_lat + (end_lat - start_lat) * progress
            lon = start_lon + (end_lon - start_lon) * progress
            
            # Calculate altitude (climbing departure)
            altitude = 1000 + 34000 * progress
            
            # Calculate speed (accelerating)
            speed = 150 + 350 * progress  # From 150 to 500 knots
            
            # Calculate heading (away from airport)
            heading = 250 - math.sin(progress * math.pi) * 15
            
            positions.append({
                'timestamp': timestamp,
                'latitude': lat,
                'longitude': lon,
                'altitude': altitude,
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
                - latitude (8 bytes): double
                - longitude (8 bytes): double
                - altitude (8 bytes): double
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
                    f.write(struct.pack('d', pos['latitude']))
                    f.write(struct.pack('d', pos['longitude']))
                    f.write(struct.pack('d', pos['altitude']))
                    f.write(struct.pack('d', pos['speed']))
                    f.write(struct.pack('d', pos['heading']))
        
        print(f"Binary file saved to: {filename}")
        print(f"Number of tracks: {len(self.tracks)}")
        for track in self.tracks:
            print(f"  - {track['track_name']} ({track['track_type']}): {len(track['positions'])} positions")


def main():
    """Generate sample binary file"""
    generator = TrackGenerator()
    generator.generate_sample_tracks()
    generator.save_to_binary('airborne_tracks.bin')
    
    # Also save as JSON for reference
    with open('airborne_tracks_reference.json', 'w') as f:
        json.dump({
            'version': '1.0',
            'tracks': generator.tracks
        }, f, indent=2)
    print("\nReference JSON saved to: airborne_tracks_reference.json")


if __name__ == '__main__':
    main()
