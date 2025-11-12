# AI Tag Generation for Airborne Tracks

## Overview

The AI Tag Generation feature uses intelligent analytics and ML-inspired algorithms to automatically classify and tag airborne tracks based on their behavior patterns. This system analyzes track data and generates descriptive tags that help in understanding aircraft behavior, flight characteristics, and operational patterns.

## Features

### 1. Speed Classification
Tags aircraft based on average speed:
- **very_slow_moving**: < 150 knots
- **slow_moving**: 150-250 knots  
- **moderate_speed**: 250-400 knots
- **fast_moving**: 400-550 knots
- **very_fast_moving**: > 550 knots
- **supersonic_capable**: Maximum speed > 600 knots
- **variable_speed**: High speed variance (σ > 50 knots)
- **constant_speed**: Low speed variance (σ < 10 knots)

### 2. G-Force & Maneuvering Analysis
Calculates G-forces from heading changes and speed to classify maneuvering intensity:
- **minimal_maneuvering**: < 2g
- **light_maneuvering_2g_4g**: 2-4g
- **moderate_maneuvering_4g_6g**: 4-6g
- **high_maneuvering_6g_8g**: 6-8g
- **extreme_maneuvering_8g_10g**: 8-10g
- **extreme_maneuvering_10g_plus**: > 10g

The G-force calculation uses:
```
G = sqrt(1 + (lateral_acceleration / g)²)
where lateral_acceleration = velocity × angular_velocity
```

### 3. Flight Path Analysis
Analyzes heading consistency to determine path linearity:
- **linear_path**: Very consistent heading (σ < 5°)
- **straight_flight**: Minimal heading deviation
- **mostly_linear**: Moderate heading changes (σ < 15°)
- **curved_path**: Significant heading changes (σ > 15°)
- **serpentine_pattern**: Highly variable heading (σ > 30°)
- **sharp_turns**: Maximum turn > 90°
- **moderate_turns**: Maximum turn > 45°

### 4. Altitude Behavior
Classifies altitude and vertical movement:
- **low_altitude**: < 10,000 ft
- **medium_altitude**: 10,000-25,000 ft
- **cruise_altitude**: 25,000-40,000 ft
- **high_altitude**: > 40,000 ft
- **level_flight**: Altitude change < 1,000 ft
- **large_altitude_change**: Altitude change > 20,000 ft
- **climbing**: Positive altitude rate
- **descending**: Negative altitude rate

### 5. Engine Configuration
Identifies aircraft engine configuration:
- **single_engine**: Single-engine aircraft (e.g., F-16, Cessna 172)
- **twin_engine**: Twin-engine aircraft (e.g., Boeing 737, 777, Airbus A320)
- **four_engine**: Four-engine aircraft (e.g., Boeing 747, Airbus A380)
- **eight_engine**: Eight-engine aircraft (e.g., B-52)

Supported aircraft types:
- Boeing 737, 777, 747
- Airbus A320, A330, A340, A380
- F-16, Cessna 172, B-52

### 6. Aircraft Role Classification
Infers operational role from behavior patterns:
- **commercial_airliner_profile**: Linear path, moderate speed, low G-forces
  - Criteria: heading_std < 10°, 250-500 kts, max_g < 2g
- **military_fighter_profile**: High speed, high G-forces
  - Criteria: max_g > 5g, speed > 400 kts
- **tactical_maneuvering**: Aggressive maneuvering patterns
  - Criteria: max_g > 3g, heading_std > 20°
- **general_aviation_profile**: Low speed, low altitude
  - Criteria: speed < 200 kts, altitude < 15,000 ft

### 7. Track Type
- **incoming_track**: Track approaching radar
- **outgoing_track**: Track departing from radar

## Usage

### Via GUI

1. **Load Binary File**: 
   - Drag & drop or browse to load a `.bin` track file
   - The file will be automatically parsed and displayed

2. **Generate AI Tags**:
   - Click the "🤖 Run AI Model generate Tags" button
   - The system will:
     - Export to CSV if not already exported
     - Analyze all tracks
     - Generate intelligent tags
     - Save tagged CSV with timestamp
     - Show statistics popup

3. **Output**:
   - Tagged CSV file: `airborne_tracks_tagged_YYYYMMDD_HHMMSS.csv`
   - Contains all original columns plus `ai_generated_tags` column
   - Tags are semicolon-separated for easy parsing

### Via Command Line

```bash
# Run standalone tag generation
python3 track_tag_generator.py

# This will:
# 1. Load airborne_tracks_extracted.csv
# 2. Generate tags for all tracks
# 3. Save to airborne_tracks_tagged_<timestamp>.csv
# 4. Display statistics
```

### Programmatic Usage

```python
from track_tag_generator import TrackTagGenerator

# Initialize generator
generator = TrackTagGenerator()

# Load CSV data
generator.load_csv('airborne_tracks_extracted.csv')

# Generate tags for all tracks
generator.generate_all_tags()

# Save tagged CSV
output_file = generator.save_tagged_csv('output.csv')

# Get tag statistics
stats = generator.get_tag_statistics()
```

## Tag Format in CSV

Tags are stored as semicolon-separated strings in the `ai_generated_tags` column:

```csv
track_id,track_name,...,ai_generated_tags
1001,INC-ALPHA-001,...,"moderate_speed; variable_speed; minimal_maneuvering; linear_path; straight_flight; medium_altitude; twin_engine; commercial_airliner_profile; incoming_track"
```

## Examples

### Commercial Airliner (Boeing 737)
```
Tags: moderate_speed, variable_speed, minimal_maneuvering, linear_path, 
      straight_flight, cruise_altitude, descending, twin_engine, 
      commercial_airliner_profile, incoming_track

Metrics:
- Average Speed: 337.5 kts
- Max G-Force: 1.00g  
- Heading Std Dev: 0.4°
- Altitude: 25,000-35,000 ft
```

### Military Fighter (Hypothetical)
```
Tags: very_fast_moving, high_maneuvering_6g_8g, curved_path, 
      sharp_turns, medium_altitude, single_engine, 
      military_fighter_profile, tactical_maneuvering

Metrics:
- Average Speed: 520 kts
- Max G-Force: 7.2g
- Heading Std Dev: 35°
- Altitude: 15,000-30,000 ft
```

### General Aviation (Cessna)
```
Tags: slow_moving, minimal_maneuvering, linear_path, 
      low_altitude, level_flight, single_engine, 
      general_aviation_profile

Metrics:
- Average Speed: 145 kts
- Max G-Force: 1.5g
- Heading Std Dev: 8°
- Altitude: 3,000-5,000 ft
```

## Technical Details

### Algorithms

1. **Speed Analysis**: Statistical analysis of speed distribution
   - Mean, max, min, standard deviation
   - Threshold-based classification

2. **G-Force Calculation**: Physics-based computation
   - Converts heading rate to angular velocity
   - Calculates lateral acceleration from turn radius
   - Computes load factor including gravity

3. **Path Analysis**: Time-series analysis of heading
   - Circular statistics for heading (handles 0°/360° wraparound)
   - Standard deviation of heading changes
   - Detection of turn patterns

4. **Altitude Behavior**: Vertical profile analysis
   - Climb/descent rate calculation
   - Altitude band classification
   - Vertical excursion measurement

5. **Aircraft Classification**: Pattern matching and heuristics
   - Aircraft type database lookup
   - Behavior-based role inference
   - Multi-criteria classification

### Performance

- Processing time: ~0.1-0.5 seconds per track
- Memory efficient: Processes tracks sequentially
- Scales to thousands of tracks

### Dependencies

```
pandas >= 1.3.0
numpy >= 1.21.0
```

## Customization

You can customize thresholds in `TrackTagGenerator` class:

```python
# Speed thresholds (knots)
self.SPEED_THRESHOLDS = {
    'very_slow': 150,
    'slow': 250,
    'moderate': 400,
    'fast': 550,
}

# G-force thresholds
self.G_FORCE_THRESHOLDS = {
    'low': 2.0,
    'moderate': 4.0,
    'high_6g': 6.0,
    'high_8g': 8.0,
    'high_10g': 10.0,
}

# Linearity threshold (degrees)
self.LINEARITY_THRESHOLD = 5.0
```

## Future Enhancements

Potential improvements:
1. Machine learning models (Random Forest, Neural Networks)
2. Weather condition integration
3. Terrain awareness tags
4. Formation flight detection
5. Anomaly detection
6. Predictive trajectory tags
7. Real-time streaming tag generation
8. Custom tag rule engine

## Troubleshooting

### No tags generated
- Ensure CSV file exists and contains valid track data
- Check that tracks have sufficient data points (minimum 2)

### Incorrect tags
- Review threshold values
- Check input data quality
- Verify timestamp intervals are consistent

### Performance issues
- Process tracks in batches
- Use filtered CSV with fewer tracks
- Increase system memory

## Support

For issues or questions:
1. Check the CSV format matches expected schema
2. Verify all required columns are present
3. Review console output for detailed analytics
4. Check tag statistics for validation

## License

Part of the Airborne Track Analysis System.
