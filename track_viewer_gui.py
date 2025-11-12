"""
Airborne Track Viewer GUI
GUI application with drag & drop, file browsing, and trajectory visualization
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime
from pathlib import Path
from track_extractor import TrackExtractor
from track_tag_generator import TrackTagGenerator


class TrackViewerGUI:
    """GUI for viewing airborne track data"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Airborne Track Viewer")
        self.root.geometry("1400x900")
        
        self.extractor = TrackExtractor()
        self.tag_generator = TrackTagGenerator()
        self.tracks = []
        self.selected_track_index = None
        self.csv_file_path = None
        
        self._setup_ui()
        self._setup_drag_drop()
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Airborne Track Viewer", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Left panel - Controls (compact layout)
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="5")
        control_frame.grid(row=1, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # File loading section
        file_frame = ttk.LabelFrame(control_frame, text="Load Binary File", padding="5")
        file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=3)
        
        # Drop zone (compact)
        self.drop_label = ttk.Label(file_frame, text="📁 Drag & Drop Here or", 
                                    relief=tk.RIDGE, padding=10, 
                                    foreground='gray', anchor=tk.CENTER)
        self.drop_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=3)
        
        # Browse button
        browse_btn = ttk.Button(file_frame, text="Browse File...", command=self._browse_file)
        browse_btn.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=3)
        
        # Current file display
        self.file_label = ttk.Label(file_frame, text="No file loaded", 
                                    foreground='gray', wraplength=250, font=('Arial', 8))
        self.file_label.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=3)
        
        # Track list section (compact)
        track_frame = ttk.LabelFrame(control_frame, text="Available Tracks", padding="5")
        track_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=3)
        
        # Track listbox with scrollbar
        list_frame = ttk.Frame(track_frame)
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        list_frame.columnconfigure(0, weight=1)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.track_listbox = tk.Listbox(list_frame, height=5, 
                                        yscrollcommand=scrollbar.set,
                                        font=('Courier', 8))
        self.track_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.track_listbox.bind('<<ListboxSelect>>', self._on_track_select)
        scrollbar.config(command=self.track_listbox.yview)
        
        # Track details section (compact)
        details_frame = ttk.LabelFrame(control_frame, text="Track Details", padding="5")
        details_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=3)
        
        self.details_text = tk.Text(details_frame, height=6, width=35, 
                                    wrap=tk.WORD, font=('Courier', 8))
        self.details_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.details_text.config(state=tk.DISABLED)
        
        # Export & AI buttons (combined for space)
        actions_frame = ttk.LabelFrame(control_frame, text="Actions", padding="5")
        actions_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=3)
        
        ttk.Button(actions_frame, text="Export JSON", 
                  command=self._export_json).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(actions_frame, text="Export CSV", 
                  command=self._export_csv).grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(actions_frame, text="Export Summary", 
                  command=self._export_summary).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # AI Tag Generation button (in same section)
        ttk.Separator(actions_frame, orient='horizontal').grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(actions_frame, text="🤖 Generate AI Tags", 
                  command=self._generate_ai_tags).grid(row=4, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Right panel - Visualization
        viz_frame = ttk.LabelFrame(main_frame, text="Track Visualization", padding="10")
        viz_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        viz_frame.columnconfigure(0, weight=1)
        viz_frame.rowconfigure(0, weight=1)
        
        # Matplotlib figure
        self.fig = Figure(figsize=(10, 8), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Toolbar
        toolbar_frame = ttk.Frame(viz_frame)
        toolbar_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        
        # Initial empty plot
        self._draw_empty_plot()
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def _setup_drag_drop(self):
        """Setup drag and drop functionality"""
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self._on_drop)
    
    def _on_drop(self, event):
        """Handle file drop event"""
        # Get the dropped file path
        file_path = event.data
        # Remove curly braces if present (Windows)
        if file_path.startswith('{') and file_path.endswith('}'):
            file_path = file_path[1:-1]
        
        self._load_file(file_path)
    
    def _browse_file(self):
        """Open file browser dialog"""
        file_path = filedialog.askopenfilename(
            title="Select Binary Track File",
            filetypes=[
                ("Binary files", "*.bin"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self._load_file(file_path)
    
    def _load_file(self, file_path):
        """Load binary file and display tracks"""
        try:
            self.status_label.config(text=f"Loading {Path(file_path).name}...")
            self.root.update()
            
            # Read binary file
            data = self.extractor.read_binary(file_path)
            self.tracks = self.extractor.get_tracks()
            
            # Update UI
            self.file_label.config(text=f"Loaded: {Path(file_path).name}", 
                                  foreground='green')
            self._populate_track_list()
            self._draw_all_tracks()
            
            self.status_label.config(text=f"Loaded {len(self.tracks)} tracks from {Path(file_path).name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
            self.status_label.config(text="Error loading file")
    
    def _populate_track_list(self):
        """Populate the track listbox"""
        self.track_listbox.delete(0, tk.END)
        
        for i, track in enumerate(self.tracks):
            track_type_icon = "🛬" if track['track_type'] == 'incoming' else "🛫"
            display_text = f"{track_type_icon} {track['track_name']} ({track['aircraft_type']})"
            self.track_listbox.insert(tk.END, display_text)
    
    def _on_track_select(self, event):
        """Handle track selection"""
        selection = self.track_listbox.curselection()
        if selection:
            self.selected_track_index = selection[0]
            self._update_track_details()
            self._draw_selected_track()
    
    def _update_track_details(self):
        """Update track details display"""
        if self.selected_track_index is None:
            return
        
        track = self.tracks[self.selected_track_index]
        
        details = f"""Track ID: {track['track_id']}
Name: {track['track_name']}
Type: {track['track_type'].upper()}
Aircraft: {track['aircraft_type']}

Start: {datetime.fromtimestamp(track['start_time']).strftime('%Y-%m-%d %H:%M:%S')}
End: {datetime.fromtimestamp(track['end_time']).strftime('%Y-%m-%d %H:%M:%S')}
Lifetime: {track['lifetime']/60:.1f} minutes

Data Points: {len(track['positions'])}

First Position:
  Range: {track['positions'][0]['range']:.2f} NM
  Azimuth: {track['positions'][0]['azimuth']:.1f}°
  Elev: {track['positions'][0]['elevation']:.0f} ft
  Speed: {track['positions'][0]['speed']:.0f} kts

Last Position:
  Range: {track['positions'][-1]['range']:.2f} NM
  Azimuth: {track['positions'][-1]['azimuth']:.1f}°
  Elev: {track['positions'][-1]['elevation']:.0f} ft
  Speed: {track['positions'][-1]['speed']:.0f} kts
"""
        
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(1.0, details)
        self.details_text.config(state=tk.DISABLED)
    
    def _draw_empty_plot(self):
        """Draw empty plot with instructions"""
        self.ax.clear()
        self.ax.text(0.5, 0.5, 'Load a binary file to view tracks', 
                    ha='center', va='center', fontsize=14, color='gray',
                    transform=self.ax.transAxes)
        self.ax.set_xlabel('X Position (NM East)')
        self.ax.set_ylabel('Y Position (NM North)')
        self.ax.set_title('Airborne Track Trajectories (Polar View)')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_aspect('equal')
        self.canvas.draw()
    
    def _polar_to_cartesian(self, range_val, azimuth):
        """Convert range/azimuth to Cartesian coordinates
        
        Args:
            range_val: Range in nautical miles
            azimuth: Azimuth in degrees (0=North, 90=East, 180=South, 270=West)
        
        Returns:
            tuple: (x, y) in nautical miles where x is East, y is North
        """
        # Convert azimuth from degrees to radians
        # Azimuth is measured clockwise from North, but we need mathematical angle
        # (counterclockwise from East)
        angle_rad = np.radians(90 - azimuth)
        
        x = range_val * np.cos(angle_rad)
        y = range_val * np.sin(angle_rad)
        
        return x, y
    
    def _draw_all_tracks(self):
        """Draw all tracks on the plot"""
        self.ax.clear()
        
        if not self.tracks:
            self._draw_empty_plot()
            return
        
        colors = {'incoming': '#2E86AB', 'outgoing': '#A23B72'}
        
        for track in self.tracks:
            # Convert polar to Cartesian coordinates
            xs = []
            ys = []
            for pos in track['positions']:
                x, y = self._polar_to_cartesian(pos['range'], pos['azimuth'])
                xs.append(x)
                ys.append(y)
            
            color = colors.get(track['track_type'], 'gray')
            
            self.ax.plot(xs, ys, color=color, alpha=0.5, linewidth=2, 
                        label=track['track_name'])
            
            # Mark start and end
            self.ax.plot(xs[0], ys[0], 'o', color=color, markersize=8, 
                        markeredgecolor='white', markeredgewidth=1.5)
            self.ax.plot(xs[-1], ys[-1], 's', color=color, markersize=8,
                        markeredgecolor='white', markeredgewidth=1.5)
        
        # Add radar origin marker
        self.ax.plot(0, 0, 'x', color='red', markersize=12, markeredgewidth=3, label='Radar Origin')
        
        self.ax.set_xlabel('X Position (NM East)', fontsize=11)
        self.ax.set_ylabel('Y Position (NM North)', fontsize=11)
        self.ax.set_title('All Airborne Track Trajectories (Polar View)', fontsize=13, fontweight='bold')
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.set_aspect('equal')
        self.ax.legend(loc='best', fontsize=9)
        
        # Add custom legend for markers
        circle = mpatches.Circle((0, 0), 0.1, color='gray', label='Start')
        square = mpatches.Rectangle((0, 0), 0.1, 0.1, color='gray', label='End')
        self.ax.legend(handles=[circle, square], loc='upper right', fontsize=9)
        
        self.canvas.draw()
    
    def _draw_selected_track(self):
        """Draw selected track highlighted among all tracks"""
        self.ax.clear()
        
        if not self.tracks or self.selected_track_index is None:
            self._draw_all_tracks()
            return
        
        colors = {'incoming': '#2E86AB', 'outgoing': '#A23B72'}
        selected_track = self.tracks[self.selected_track_index]
        
        # Draw all tracks in light gray
        for i, track in enumerate(self.tracks):
            xs = []
            ys = []
            for pos in track['positions']:
                x, y = self._polar_to_cartesian(pos['range'], pos['azimuth'])
                xs.append(x)
                ys.append(y)
            
            if i == self.selected_track_index:
                continue
            
            self.ax.plot(xs, ys, color='lightgray', alpha=0.3, linewidth=1.5)
            self.ax.plot(xs[0], ys[0], 'o', color='lightgray', markersize=6, alpha=0.5)
            self.ax.plot(xs[-1], ys[-1], 's', color='lightgray', markersize=6, alpha=0.5)
        
        # Draw selected track highlighted
        sel_xs = []
        sel_ys = []
        sel_elevs = []
        for pos in selected_track['positions']:
            x, y = self._polar_to_cartesian(pos['range'], pos['azimuth'])
            sel_xs.append(x)
            sel_ys.append(y)
            sel_elevs.append(pos['elevation'])
        
        sel_color = colors.get(selected_track['track_type'], 'red')
        
        # Draw track with color gradient based on elevation
        for i in range(len(sel_xs) - 1):
            self.ax.plot(sel_xs[i:i+2], sel_ys[i:i+2], 
                        color=sel_color, linewidth=3, alpha=0.8)
        
        # Mark waypoints every 10 points
        for i in range(0, len(sel_xs), 10):
            self.ax.plot(sel_xs[i], sel_ys[i], 'o', color=sel_color, 
                        markersize=4, alpha=0.6)
        
        # Highlight start and end
        self.ax.plot(sel_xs[0], sel_ys[0], 'o', color='green', markersize=12, 
                    markeredgecolor='white', markeredgewidth=2, label='Start', zorder=10)
        self.ax.plot(sel_xs[-1], sel_ys[-1], 's', color='red', markersize=12,
                    markeredgecolor='white', markeredgewidth=2, label='End', zorder=10)
        
        # Add direction arrows
        arrow_interval = max(1, len(sel_xs) // 5)
        for i in range(arrow_interval, len(sel_xs) - 1, arrow_interval):
            dx = sel_xs[i+1] - sel_xs[i]
            dy = sel_ys[i+1] - sel_ys[i]
            # Normalize arrow length
            arrow_length = np.sqrt(dx**2 + dy**2)
            if arrow_length > 0:
                scale = 5.0 / arrow_length  # Fixed arrow length of 5 NM
                self.ax.arrow(sel_xs[i], sel_ys[i], dx*scale*0.3, dy*scale*0.3,
                             head_width=2, head_length=2, fc=sel_color, 
                             ec=sel_color, alpha=0.7)
        
        # Add radar origin marker
        self.ax.plot(0, 0, 'x', color='red', markersize=12, markeredgewidth=3, label='Radar Origin')
        
        self.ax.set_xlabel('X Position (NM East)', fontsize=11)
        self.ax.set_ylabel('Y Position (NM North)', fontsize=11)
        
        track_type_text = "INCOMING" if selected_track['track_type'] == 'incoming' else "OUTGOING"
        self.ax.set_title(f"Selected Track: {selected_track['track_name']} ({track_type_text})", 
                         fontsize=13, fontweight='bold')
        
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.set_aspect('equal')
        self.ax.legend(loc='best', fontsize=10)
        
        self.canvas.draw()
    
    def _export_json(self):
        """Export tracks to JSON"""
        if not self.tracks:
            messagebox.showwarning("Warning", "No tracks loaded")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            self.extractor.export_to_json(filename)
            messagebox.showinfo("Success", f"Exported to:\n{filename}")
    
    def _export_csv(self):
        """Export tracks to CSV"""
        if not self.tracks:
            messagebox.showwarning("Warning", "No tracks loaded")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            self.extractor.export_to_csv(filename)
            self.csv_file_path = filename
            messagebox.showinfo("Success", f"Exported to:\n{filename}")
    
    def _export_summary(self):
        """Export track summary"""
        if not self.tracks:
            messagebox.showwarning("Warning", "No tracks loaded")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            self.extractor.export_summary(filename)
            messagebox.showinfo("Success", f"Exported to:\n{filename}")
    
    def _generate_ai_tags(self):
        """Generate AI tags for tracks"""
        if not self.tracks:
            messagebox.showwarning("Warning", "No tracks loaded")
            return
        
        # Check if CSV has been exported
        if self.csv_file_path is None or not Path(self.csv_file_path).exists():
            # Export to temporary CSV first
            self.csv_file_path = 'airborne_tracks_extracted.csv'
            self.extractor.export_to_csv(self.csv_file_path)
        
        try:
            self.status_label.config(text="Generating AI tags... Please wait...")
            self.root.update()
            
            # Generate tags
            self.tag_generator.load_csv(self.csv_file_path)
            self.tag_generator.generate_all_tags()
            
            # Save tagged CSV
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'airborne_tracks_tagged_{timestamp}.csv'
            self.tag_generator.save_tagged_csv(output_file)
            
            # Show statistics in a popup
            tag_stats = self.tag_generator.get_tag_statistics()
            
            # Create summary message
            summary = f"AI Tag Generation Complete!\n\n"
            summary += f"Tagged file saved to:\n{output_file}\n\n"
            summary += f"Total tracks analyzed: {self.tag_generator.df['track_id'].nunique()}\n"
            summary += f"Total data points: {len(self.tag_generator.df)}\n"
            summary += f"Unique tags generated: {len(tag_stats)}\n\n"
            summary += "Top 5 most common tags:\n"
            for tag, count in list(tag_stats.most_common(5)):
                summary += f"  • {tag}: {count}\n"
            
            messagebox.showinfo("AI Tag Generation Complete", summary)
            self.status_label.config(text=f"AI tags generated and saved to {output_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate AI tags:\n{str(e)}")
            self.status_label.config(text="Error generating AI tags")
    
    def _set_csv_path(self, path):
        """Set the CSV file path after export"""
        self.csv_file_path = path


def main():
    """Launch the GUI application"""
    root = TkinterDnD.Tk()
    app = TrackViewerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
