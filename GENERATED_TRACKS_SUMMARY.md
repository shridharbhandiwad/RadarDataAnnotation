# 5 Diverse Airborne Tracks - Generation Summary

**Generated on:** 2025-11-12  
**Files Created:**
- `airborne_tracks.bin` - Binary track data
- `airborne_tracks_reference.json` - JSON reference
- `airborne_tracks_extracted.csv` - Extracted track data
- `airborne_tracks_tagged_20251112_145001.csv` - Tracks with AI-generated tags

---

## Track Overview

### 1. FIGHTER-RAPTOR-001 (Military Fighter)
- **Aircraft:** F-16 (Single Engine)
- **Type:** Incoming
- **Duration:** 50.0 minutes (100 positions)
- **Speed:** 400-700 knots (avg: 550 knots)
- **Altitude:** 30,003-40,000 feet (cruise altitude)
- **Characteristics:** Supersonic capable, variable speed, curved flight path

**Tags (8):**
- very_fast_moving
- variable_speed
- supersonic_capable
- minimal_maneuvering
- curved_path
- cruise_altitude
- single_engine
- incoming_track

---

### 2. COMM-DELTA-452 (Commercial Airliner)
- **Aircraft:** Boeing 777 (Twin Engine)
- **Type:** Incoming
- **Duration:** 45.0 minutes (90 positions)
- **Speed:** 450-460 knots (avg: 456 knots)
- **Altitude:** 36,000-36,200 feet (level cruise)
- **Characteristics:** Constant speed, linear path, level flight

**Tags (9):**
- fast_moving
- constant_speed
- linear_path
- straight_flight
- cruise_altitude
- level_flight
- twin_engine
- commercial_airliner_profile
- incoming_track

---

### 3. GA-CESSNA-N12345 (General Aviation)
- **Aircraft:** Cessna 172 (Single Engine)
- **Type:** Outgoing
- **Duration:** 40.0 minutes (80 positions)
- **Speed:** 85-135 knots (avg: 115 knots)
- **Altitude:** 5,001-10,999 feet (low altitude)
- **Characteristics:** Very slow, low altitude, mostly linear path

**Tags (7):**
- very_slow_moving
- minimal_maneuvering
- mostly_linear
- low_altitude
- single_engine
- general_aviation_profile
- outgoing_track

---

### 4. BOMBER-BUFF-52 (Strategic Bomber)
- **Aircraft:** B-52 (Eight Engines)
- **Type:** Outgoing
- **Duration:** 60.0 minutes (120 positions)
- **Speed:** 380-460 knots (avg: 420 knots)
- **Altitude:** 5,000-45,000 feet (large altitude change)
- **Characteristics:** Fast, climbing, straight flight, large altitude change

**Tags (10):**
- fast_moving
- minimal_maneuvering
- linear_path
- straight_flight
- medium_altitude
- large_altitude_change
- climbing
- eight_engine
- commercial_airliner_profile
- outgoing_track

---

### 5. CARGO-JUMBO-747F (Cargo Aircraft)
- **Aircraft:** Boeing 747 (Four Engines)
- **Type:** Incoming
- **Duration:** 50.0 minutes (100 positions)
- **Speed:** 180-420 knots (avg: 300 knots)
- **Altitude:** 6,000-38,000 feet (descending)
- **Characteristics:** Variable speed, descending, large altitude change

**Tags (11):**
- moderate_speed
- variable_speed
- minimal_maneuvering
- linear_path
- straight_flight
- medium_altitude
- large_altitude_change
- descending
- four_engine
- commercial_airliner_profile
- incoming_track

---

## Tag Coverage Summary

**Total Unique Tags Generated:** 27

### Speed Tags (7)
- very_slow_moving
- moderate_speed
- fast_moving
- very_fast_moving
- constant_speed
- variable_speed
- supersonic_capable

### Maneuvering Tags (1)
- minimal_maneuvering

### Path/Flight Pattern Tags (5)
- linear_path
- straight_flight
- mostly_linear
- curved_path
- level_flight

### Altitude Tags (7)
- low_altitude
- medium_altitude
- cruise_altitude
- level_flight
- large_altitude_change
- climbing
- descending

### Engine Configuration Tags (4)
- single_engine
- twin_engine
- four_engine
- eight_engine

### Aircraft Role Tags (2)
- general_aviation_profile
- commercial_airliner_profile

### Track Type Tags (2)
- incoming_track
- outgoing_track

---

## Design Strategy

These 5 tracks were specifically designed to trigger a diverse set of AI-generated tags:

1. **Military Fighter** - Demonstrates supersonic capability, variable speed, and curved paths
2. **Commercial Airliner** - Shows constant speed, level flight, and linear paths typical of commercial aviation
3. **General Aviation** - Illustrates slow-moving, low-altitude flight patterns
4. **Strategic Bomber** - Features large altitude changes (climbing) and eight-engine configuration
5. **Cargo Aircraft** - Exhibits variable speed, descending profile, and four-engine configuration

The tracks successfully generated **27 unique tags** covering all major tag categories including speed, maneuvering, path patterns, altitude behavior, engine configurations, and aircraft roles.

---

## Files Generated

- **Binary Format:** `airborne_tracks.bin` (490 total data points)
- **JSON Reference:** `airborne_tracks_reference.json`
- **CSV Extract:** `airborne_tracks_extracted.csv`
- **Tagged CSV:** `airborne_tracks_tagged_20251112_145001.csv`

All files are ready for viewing in the GUI (`track_viewer_gui.py`) or further analysis.
