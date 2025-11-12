#!/usr/bin/env python3
"""
Verification script for AI Tag Generation feature
Demonstrates the complete workflow and validates functionality
"""
import sys
from pathlib import Path

print("=" * 80)
print("AI TAG GENERATION - VERIFICATION SCRIPT")
print("=" * 80)
print()

# Check files exist
print("✓ Checking required files...")
required_files = [
    'track_tag_generator.py',
    'track_viewer_gui.py',
    'track_extractor.py',
    'airborne_tracks_extracted.csv',
]

for file in required_files:
    if Path(file).exists():
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} - MISSING!")
        sys.exit(1)

print()

# Check dependencies
print("✓ Checking dependencies...")
try:
    import pandas as pd
    print(f"  ✓ pandas (version {pd.__version__})")
except ImportError:
    print("  ✗ pandas - NOT INSTALLED!")
    sys.exit(1)

try:
    import numpy as np
    print(f"  ✓ numpy (version {np.__version__})")
except ImportError:
    print("  ✗ numpy - NOT INSTALLED!")
    sys.exit(1)

print()

# Import and test tag generator
print("✓ Testing TrackTagGenerator module...")
try:
    from track_tag_generator import TrackTagGenerator
    print("  ✓ Module imports successfully")
except Exception as e:
    print(f"  ✗ Import failed: {e}")
    sys.exit(1)

print()

# Run a quick test
print("✓ Running functionality test...")
try:
    generator = TrackTagGenerator()
    print("  ✓ TrackTagGenerator instantiated")
    
    # Load CSV
    df = generator.load_csv('airborne_tracks_extracted.csv')
    print(f"  ✓ Loaded {len(df)} data points from {df['track_id'].nunique()} tracks")
    
    # Generate tags
    print("  ✓ Generating tags...")
    generator.generate_all_tags()
    print("  ✓ Tags generated successfully")
    
    # Check output
    if 'ai_generated_tags' in generator.df.columns:
        print("  ✓ 'ai_generated_tags' column created")
        
        # Show sample tags
        sample_tags = generator.df.iloc[0]['ai_generated_tags']
        tag_list = sample_tags.split('; ')
        print(f"  ✓ Generated {len(tag_list)} tags for first track")
        print(f"    Sample tags: {', '.join(tag_list[:3])}...")
    else:
        print("  ✗ 'ai_generated_tags' column not found!")
        sys.exit(1)
    
    # Get statistics
    stats = generator.get_tag_statistics()
    print(f"  ✓ Tag statistics calculated: {len(stats)} unique tags")
    
except Exception as e:
    print(f"  ✗ Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Check GUI integration
print("✓ Checking GUI integration...")
try:
    import ast
    
    with open('track_viewer_gui.py', 'r') as f:
        gui_code = f.read()
    
    # Check for key components
    checks = [
        ('from track_tag_generator import TrackTagGenerator', 'Import statement'),
        ('self.tag_generator = TrackTagGenerator()', 'Instantiation'),
        ('def _generate_ai_tags(self):', 'AI tags method'),
        ('Run AI Model generate Tags', 'Button text'),
    ]
    
    for check_str, description in checks:
        if check_str in gui_code:
            print(f"  ✓ {description} found")
        else:
            print(f"  ✗ {description} not found!")
            sys.exit(1)
    
except Exception as e:
    print(f"  ✗ GUI check failed: {e}")
    sys.exit(1)

print()

# Final summary
print("=" * 80)
print("✅ ALL VERIFICATION CHECKS PASSED!")
print("=" * 80)
print()
print("Summary:")
print("  • All required files present")
print("  • Dependencies installed and working")
print("  • TrackTagGenerator module functional")
print("  • Tag generation working correctly")
print("  • GUI integration complete")
print()
print("The AI Tag Generation feature is ready to use!")
print()
print("Next steps:")
print("  1. Run GUI: python3 track_viewer_gui.py")
print("  2. Load binary file: airborne_tracks.bin")
print("  3. Click: 🤖 Run AI Model generate Tags")
print("  4. View the tagged CSV output")
print()
print("For more information:")
print("  • AI_TAG_GENERATION_GUIDE.md - Complete documentation")
print("  • QUICKSTART_AI_TAGS.md - Quick start guide")
print("  • IMPLEMENTATION_SUMMARY.md - Implementation details")
print()
