# Finding the AI Tag Generation Button

## The Issue
The **"🤖 Run AI Model generate Tags"** button was getting cut off at the bottom of the control panel on smaller screens or when the window was resized.

## The Fix
Added a **scrollbar** to the left Controls panel so you can access all buttons regardless of window size.

## How to See the Button

1. **Launch the GUI:**
   ```bash
   ./run_gui.sh
   # or
   python3 track_viewer_gui.py
   ```

2. **Look at the left panel** labeled "Controls"

3. **You should see a scrollbar** on the right side of the Controls panel

4. **Scroll down** using:
   - Mouse wheel
   - Click and drag the scrollbar
   - Arrow keys (if the panel is focused)

5. **The button is at the bottom** in a section called "AI Tag Generation"

## Control Panel Layout (Top to Bottom)

```
┌─ Controls ─────────────────────┐
│ 1. Load Binary File            │
│    - Drag & Drop zone          │
│    - Browse button             │
│    - File status               │
│                                 │
│ 2. Available Tracks            │
│    - Track list                │
│                                 │
│ 3. Track Details               │
│    - Details text box          │
│                                 │
│ 4. Export                      │
│    - Export to JSON            │
│    - Export to CSV             │
│    - Export Summary            │
│                                 │
│ 5. AI Tag Generation     ⬅️ SCROLL DOWN TO HERE
│    - 🤖 Run AI Model     ⬅️ YOUR BUTTON!
│      generate Tags             │
└─────────────────────────────────┘
```

## Button Functionality

When you click the **"🤖 Run AI Model generate Tags"** button:
1. It will export your tracks to CSV (if not already done)
2. Run AI analysis to generate descriptive tags
3. Save a new file: `airborne_tracks_tagged_YYYYMMDD_HHMMSS.csv`
4. Show you statistics about the generated tags

## Still Can't See It?

If you still can't see the button after scrolling:

1. **Make the window taller** - Drag the bottom edge down
2. **Check the window size** - Should be at least 900px tall
3. **Restart the GUI** - Close and reopen it
4. **Check for errors** - Look at the terminal for any error messages

## Verification

Run this command to verify the button exists in the code:
```bash
grep "🤖 Run AI Model generate Tags" track_viewer_gui.py
```

You should see:
```python
ttk.Button(ai_frame, text="🤖 Run AI Model generate Tags",
```
