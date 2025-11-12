"""
AI Model Tag Generator for Airborne Tracks
Analyzes track behavior and generates intelligent tags
"""
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import csv


class TrackTagGenerator:
    """Generate intelligent tags for airborne tracks using ML/analytics"""
    
    def __init__(self):
        self.df = None
        self.tags_generated = False
        
        # Thresholds for classification
        self.SPEED_THRESHOLDS = {
            'very_slow': 150,    # < 150 knots
            'slow': 250,         # 150-250 knots
            'moderate': 400,     # 250-400 knots
            'fast': 550,         # 400-550 knots
            # > 550 knots = very_fast
        }
        
        self.G_FORCE_THRESHOLDS = {
            'low': 2.0,      # < 2g - normal flight
            'moderate': 4.0,  # 2-4g - moderate maneuvering
            'high_6g': 6.0,   # 4-6g - high maneuvering
            'high_8g': 8.0,   # 6-8g - very high maneuvering
            'high_10g': 10.0, # 8-10g - extreme maneuvering
            # > 10g = extreme_10g_plus
        }
        
        self.LINEARITY_THRESHOLD = 5.0  # degrees - heading deviation threshold
        
        # Aircraft engine configuration mapping
        self.ENGINE_CONFIG = {
            'Boeing 737': 'twin_engine',
            'Airbus A320': 'twin_engine',
            'Boeing 777': 'twin_engine',
            'Airbus A380': 'four_engine',
            'Boeing 747': 'four_engine',
            'Cessna 172': 'single_engine',
            'F-16': 'single_engine',
            'B-52': 'eight_engine',
        }
    
    def load_csv(self, csv_file):
        """Load CSV file containing track data"""
        print(f"\n{'='*80}")
        print(f"Loading track data from: {csv_file}")
        print(f"{'='*80}")
        
        self.df = pd.read_csv(csv_file)
        print(f"✓ Loaded {len(self.df)} data points from {self.df['track_id'].nunique()} tracks")
        return self.df
    
    def calculate_speed_tags(self, track_data):
        """Calculate speed-based tags"""
        speeds = track_data['speed'].values
        avg_speed = np.mean(speeds)
        max_speed = np.max(speeds)
        min_speed = np.min(speeds)
        speed_variance = np.std(speeds)
        
        tags = []
        
        # Average speed classification
        if avg_speed < self.SPEED_THRESHOLDS['very_slow']:
            tags.append('very_slow_moving')
        elif avg_speed < self.SPEED_THRESHOLDS['slow']:
            tags.append('slow_moving')
        elif avg_speed < self.SPEED_THRESHOLDS['moderate']:
            tags.append('moderate_speed')
        elif avg_speed < self.SPEED_THRESHOLDS['fast']:
            tags.append('fast_moving')
        else:
            tags.append('very_fast_moving')
        
        # Speed variability
        if speed_variance > 50:
            tags.append('variable_speed')
        elif speed_variance < 10:
            tags.append('constant_speed')
        
        # Extreme speeds
        if max_speed > 600:
            tags.append('supersonic_capable')
        
        return tags, {'avg_speed': avg_speed, 'max_speed': max_speed, 
                     'min_speed': min_speed, 'speed_std': speed_variance}
    
    def calculate_g_forces(self, track_data):
        """Calculate G-forces from heading and speed changes"""
        headings = track_data['heading'].values
        speeds = track_data['speed'].values  # knots
        
        if len(headings) < 3:
            return [], {'max_g': 0, 'avg_g': 0}
        
        # Convert speed from knots to m/s (1 knot = 0.514444 m/s)
        speeds_ms = speeds * 0.514444
        
        # Calculate heading change rate (degrees per sample)
        heading_changes = np.diff(headings)
        
        # Handle wraparound (e.g., 359° to 1°)
        heading_changes = np.where(heading_changes > 180, heading_changes - 360, heading_changes)
        heading_changes = np.where(heading_changes < -180, heading_changes + 360, heading_changes)
        
        # Estimate turn radius and G-force
        # For a coordinated turn: G = sqrt(1 + (V^2 / (g * r))^2)
        # Simplified: lateral_g ≈ V * heading_rate / g
        
        g_forces = []
        dt = 30  # Time between samples in seconds (from the data pattern)
        
        for i in range(len(heading_changes)):
            if abs(heading_changes[i]) > 0.1:  # Ignore very small changes
                # heading_rate in rad/s
                heading_rate = np.radians(abs(heading_changes[i])) / dt
                v = speeds_ms[i] if i < len(speeds_ms) else speeds_ms[-1]
                
                # Lateral acceleration: a = v * ω (where ω is angular velocity)
                lateral_accel = v * heading_rate
                
                # Convert to G-force (1g ≈ 9.81 m/s²)
                g_force = lateral_accel / 9.81
                
                # Add 1g for gravity (total load factor)
                total_g = np.sqrt(1 + g_force**2)
                g_forces.append(total_g)
        
        if not g_forces:
            return [], {'max_g': 0, 'avg_g': 0}
        
        max_g = np.max(g_forces)
        avg_g = np.mean(g_forces)
        
        tags = []
        
        # Classify based on maximum G-force experienced
        if max_g > self.G_FORCE_THRESHOLDS['high_10g']:
            tags.append('extreme_maneuvering_10g_plus')
        elif max_g > self.G_FORCE_THRESHOLDS['high_8g']:
            tags.append('extreme_maneuvering_8g_10g')
        elif max_g > self.G_FORCE_THRESHOLDS['high_6g']:
            tags.append('high_maneuvering_6g_8g')
        elif max_g > self.G_FORCE_THRESHOLDS['moderate']:
            tags.append('moderate_maneuvering_4g_6g')
        elif max_g > self.G_FORCE_THRESHOLDS['low']:
            tags.append('light_maneuvering_2g_4g')
        else:
            tags.append('minimal_maneuvering')
        
        return tags, {'max_g': max_g, 'avg_g': avg_g}
    
    def calculate_linearity(self, track_data):
        """Determine if track follows a linear path"""
        headings = track_data['heading'].values
        
        if len(headings) < 3:
            return [], {'heading_std': 0}
        
        # Calculate heading standard deviation
        # Handle circular nature of headings
        heading_changes = np.diff(headings)
        heading_changes = np.where(heading_changes > 180, heading_changes - 360, heading_changes)
        heading_changes = np.where(heading_changes < -180, heading_changes + 360, heading_changes)
        
        heading_std = np.std(heading_changes)
        
        tags = []
        
        if heading_std < self.LINEARITY_THRESHOLD:
            tags.append('linear_path')
            tags.append('straight_flight')
        elif heading_std < 15:
            tags.append('mostly_linear')
        else:
            tags.append('curved_path')
            
        # Check for specific patterns
        if heading_std > 30:
            tags.append('serpentine_pattern')
        
        # Check for turns
        max_heading_change = np.max(np.abs(heading_changes))
        if max_heading_change > 90:
            tags.append('sharp_turns')
        elif max_heading_change > 45:
            tags.append('moderate_turns')
        
        return tags, {'heading_std': heading_std, 'max_turn': max_heading_change}
    
    def calculate_altitude_behavior(self, track_data):
        """Analyze altitude behavior"""
        elevations = track_data['elevation'].values
        
        if len(elevations) < 2:
            return [], {'elevation_change': 0}
        
        max_elev = np.max(elevations)
        min_elev = np.min(elevations)
        elevation_change = max_elev - min_elev
        avg_elev = np.mean(elevations)
        
        # Calculate climb/descent rates
        elev_changes = np.diff(elevations)
        
        tags = []
        
        # Altitude classification
        if avg_elev > 40000:
            tags.append('high_altitude')
        elif avg_elev > 25000:
            tags.append('cruise_altitude')
        elif avg_elev > 10000:
            tags.append('medium_altitude')
        else:
            tags.append('low_altitude')
        
        # Altitude change patterns
        if elevation_change < 1000:
            tags.append('level_flight')
        elif elevation_change > 20000:
            tags.append('large_altitude_change')
        
        # Climbing or descending
        if np.mean(elev_changes) > 100:
            tags.append('climbing')
        elif np.mean(elev_changes) < -100:
            tags.append('descending')
        
        return tags, {'elevation_change': elevation_change, 'avg_elevation': avg_elev}
    
    def get_engine_configuration(self, aircraft_type):
        """Determine engine configuration based on aircraft type"""
        for aircraft_model, engine_config in self.ENGINE_CONFIG.items():
            if aircraft_model.lower() in aircraft_type.lower():
                return [engine_config], {'engine_config': engine_config}
        
        # Default classification based on common patterns
        if any(x in aircraft_type.lower() for x in ['737', 'a320', '777', '787', 'a330']):
            return ['twin_engine'], {'engine_config': 'twin_engine'}
        elif any(x in aircraft_type.lower() for x in ['747', 'a380', 'a340']):
            return ['four_engine'], {'engine_config': 'four_engine'}
        else:
            return ['unknown_engine_config'], {'engine_config': 'unknown'}
    
    def classify_aircraft_role(self, track_data):
        """Infer aircraft role from behavior"""
        tags = []
        
        # Get all other metrics
        _, speed_metrics = self.calculate_speed_tags(track_data)
        _, g_metrics = self.calculate_g_forces(track_data)
        _, linearity_metrics = self.calculate_linearity(track_data)
        _, altitude_metrics = self.calculate_altitude_behavior(track_data)
        
        avg_speed = speed_metrics['avg_speed']
        max_g = g_metrics['max_g']
        heading_std = linearity_metrics['heading_std']
        
        # Military/Fighter characteristics
        if max_g > 5 and avg_speed > 400:
            tags.append('military_fighter_profile')
        elif max_g > 3 and heading_std > 20:
            tags.append('tactical_maneuvering')
        
        # Commercial airliner characteristics
        if heading_std < 10 and 250 < avg_speed < 500 and max_g < 2:
            tags.append('commercial_airliner_profile')
        
        # General aviation
        if avg_speed < 200 and altitude_metrics['avg_elevation'] < 15000:
            tags.append('general_aviation_profile')
        
        return tags
    
    def generate_tags_for_track(self, track_id):
        """Generate all tags for a single track"""
        track_data = self.df[self.df['track_id'] == track_id]
        
        if track_data.empty:
            return []
        
        all_tags = []
        metrics = {}
        
        # Speed tags
        speed_tags, speed_metrics = self.calculate_speed_tags(track_data)
        all_tags.extend(speed_tags)
        metrics.update(speed_metrics)
        
        # G-force tags
        g_tags, g_metrics = self.calculate_g_forces(track_data)
        all_tags.extend(g_tags)
        metrics.update(g_metrics)
        
        # Linearity tags
        linearity_tags, linearity_metrics = self.calculate_linearity(track_data)
        all_tags.extend(linearity_tags)
        metrics.update(linearity_metrics)
        
        # Altitude tags
        altitude_tags, altitude_metrics = self.calculate_altitude_behavior(track_data)
        all_tags.extend(altitude_tags)
        metrics.update(altitude_metrics)
        
        # Engine configuration
        aircraft_type = track_data.iloc[0]['aircraft_type']
        engine_tags, engine_metrics = self.get_engine_configuration(aircraft_type)
        all_tags.extend(engine_tags)
        metrics.update(engine_metrics)
        
        # Aircraft role classification
        role_tags = self.classify_aircraft_role(track_data)
        all_tags.extend(role_tags)
        
        # Track type tag
        track_type = track_data.iloc[0]['track_type']
        all_tags.append(f"{track_type}_track")
        
        return all_tags, metrics
    
    def generate_all_tags(self):
        """Generate tags for all tracks in the dataset"""
        if self.df is None:
            raise ValueError("No data loaded. Call load_csv() first.")
        
        print(f"\n{'='*80}")
        print("GENERATING AI TAGS FOR ALL TRACKS")
        print(f"{'='*80}\n")
        
        track_ids = self.df['track_id'].unique()
        
        # Store tags for each row
        tags_list = []
        
        for track_id in track_ids:
            track_name = self.df[self.df['track_id'] == track_id].iloc[0]['track_name']
            print(f"Analyzing Track {track_id} ({track_name})...")
            
            tags, metrics = self.generate_tags_for_track(track_id)
            
            # Print summary
            print(f"  ✓ Generated {len(tags)} tags")
            print(f"    Speed: {metrics['avg_speed']:.1f} kts (max: {metrics['max_speed']:.1f})")
            print(f"    G-Force: {metrics['max_g']:.2f}g (avg: {metrics['avg_g']:.2f})")
            print(f"    Path: heading_std={metrics['heading_std']:.1f}°")
            print(f"    Tags: {', '.join(tags[:5])}{'...' if len(tags) > 5 else ''}")
            print()
            
            # Add tags to each row of this track
            track_indices = self.df[self.df['track_id'] == track_id].index
            for idx in track_indices:
                tags_list.append('; '.join(tags))
        
        # Add tags column to dataframe
        self.df['ai_generated_tags'] = tags_list
        self.tags_generated = True
        
        print(f"{'='*80}")
        print(f"✓ AI TAG GENERATION COMPLETE!")
        print(f"{'='*80}\n")
        
        return self.df
    
    def save_tagged_csv(self, output_file=None):
        """Save the CSV with generated tags"""
        if not self.tags_generated:
            raise ValueError("Tags not generated yet. Call generate_all_tags() first.")
        
        if output_file is None:
            # Create output filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'airborne_tracks_tagged_{timestamp}.csv'
        
        self.df.to_csv(output_file, index=False)
        print(f"✓ Saved tagged data to: {output_file}")
        print(f"  Total rows: {len(self.df)}")
        print(f"  Total tracks: {self.df['track_id'].nunique()}")
        
        return output_file
    
    def get_tag_statistics(self):
        """Get statistics about generated tags"""
        if not self.tags_generated:
            return None
        
        all_tags = []
        for tags_str in self.df['ai_generated_tags'].unique():
            all_tags.extend(tags_str.split('; '))
        
        from collections import Counter
        tag_counts = Counter(all_tags)
        
        print(f"\n{'='*80}")
        print("TAG STATISTICS")
        print(f"{'='*80}")
        print(f"Total unique tag combinations: {self.df['ai_generated_tags'].nunique()}")
        print(f"Total unique tags: {len(tag_counts)}")
        print(f"\nMost common tags:")
        for tag, count in tag_counts.most_common(10):
            print(f"  {tag:40s}: {count:3d} occurrences")
        print(f"{'='*80}\n")
        
        return tag_counts


def main():
    """Demo tag generation"""
    generator = TrackTagGenerator()
    
    # Check if CSV file exists
    csv_file = 'airborne_tracks_extracted.csv'
    if not Path(csv_file).exists():
        print(f"Error: {csv_file} not found!")
        print("Please run track_extractor.py first to create the CSV file.")
        return
    
    # Load CSV
    generator.load_csv(csv_file)
    
    # Generate tags
    generator.generate_all_tags()
    
    # Save tagged CSV
    output_file = generator.save_tagged_csv()
    
    # Show statistics
    generator.get_tag_statistics()
    
    print("\n" + "="*80)
    print("TAG GENERATION COMPLETE!")
    print("="*80)
    print(f"\nTagged CSV saved to: {output_file}")
    print("\nYou can now load this file in the GUI or use it for further analysis.")


if __name__ == '__main__':
    main()
