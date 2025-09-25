
# --- Imports ---

import json # To read the JSON file
import tkinter as tk # To draw the GUI
import random # To pick random colours
import math # Imports module for mathematic operations

# --- Definitions ---

canvas_width = 1500
canvas_height = 1080
margin = 80
freq_line_y_coordinates = [200, 400, 600, 800]
freq_line_width = 2
row_height = 18

line_ranges = {
    0: {"min": 0, "max": 50000},
    1: {"min": 50000, "max": 200000},
    2: {"min": 200000, "max": 400000},
    3: {"min": 400000, "max": 600000} }

# --- Custom tick positions for each line ---
line_ticks_custom = {
    0: [0, 12.1, 52, 147, 694, 2700, 11200, 50000],     # ticks for line 0
    1: [50000, 78000, 122000, 141000, 200000],            # ticks for line 1
    2: [200000, 238000, 275000, 342000, 400000],            # ticks for line 2
    3: [400000, 442000, 546000, 568000, 600000]          # ticks for line 3 ¨
}


# Fetch data

with open("data.json", "r", encoding="utf-8") as f: # opens data.json as f in read mode with encoding method utf-8 
    raw = json.load(f) # Load list of dicts from file

# Convert to a simpler list of tuples: (start_MHz, end_MHz, label)

bands = [] # creates an empty list called bands

for b in raw:
    start = float(b["startfrekvens"]) # sets variable start to "startfrekvens" in current band converted to floating number
    end = float(b["slutfrekvens"]) # sets variable end to "slutfrekvens" in current band converted to floating number
    label = b["användningsområde"] # sets variable label to "användningsområde" in current band converted to floating number
    if end > start: # skip bad rows
        bands.append((start, end, label)) # adds variables to bands

# --- Tkinter setup ---

root = tk.Tk() # create root window
root.title("Swedish Freqeuncy Allocation") # sets root title as "Swedish Freqeuncy Allocation"
c = tk.Canvas(root, width = canvas_width, height = canvas_height, background = "white") # creates a canvas in root (with specifications)
c.pack() # makes canvas visible by setting geometry managing method to pack

# --- Functions ---

def freqToPixelX(freq, min_f, max_f):

    """

    Maps a frequency (in MHz) to a x-coordinate.

    Arguments:
        "freq"

    Returns:
        "pixel_x"

    """

    log_min = math.log10(max(min_f, 1))  # avoid log(0)
    log_max = math.log10(max_f)
    log_freq = math.log10(max(freq, 1))

    pixel_x = margin + (log_freq - log_min) / (log_max - log_min) * (canvas_width - 2 * margin)
    return pixel_x


def draw_custom_ticks_log(y, line_index, min_f, max_f):
    """Draw user-defined ticks on a logarithmic axis."""
    ticks = line_ticks_custom.get(line_index, [])
    for tick in ticks:
        if min_f <= tick <= max_f:
            x = freqToPixelX(tick, min_f, max_f)
            c.create_line(x, y - 5, x, y + 5)
            c.create_text(x, y + 15, text=f"{tick:g} MHz", font=("Arial", 7)) 


# Draw axis

for y in freq_line_y_coordinates:
    c.create_line(margin, y, canvas_width - margin, y, width = freq_line_width) 

def get_line_index(freq):

    """

    Maps a frequency to one of the four frequency lines.

    Arguments: 
        "freq"

    Returns:
        "line_index"
    
    """

    if freq <= 50000:
        return 0 
    elif freq <= 200000:
        return 1
    elif freq <= 400000:
        return 2
    else:
        return 3 

for line_index, y in enumerate(freq_line_y_coordinates):
    min_f = line_ranges[line_index]["min"]
    max_f = line_ranges[line_index]["max"]
    c.create_line(margin, y, canvas_width - margin, y, width=freq_line_width)
    draw_custom_ticks_log(y, line_index, min_f, max_f) 

# Loop through bands, find first empty row, random color
rows_per_line = [[] for _ in range(len(freq_line_y_coordinates))] 

for start, end, label in bands:
    # Loop through all frequency lines
    for line_index in range(len(freq_line_y_coordinates)):
        min_f = line_ranges[line_index]["min"]
        max_f = line_ranges[line_index]["max"]

        # Compute overlap between the band and this line's range
        seg_start = max(start, min_f)
        seg_end   = min(end, max_f)

        if seg_end <= seg_start:
            continue  # skip if no overlap with this line

        # Now handle placement of this segment
        rows = rows_per_line[line_index]
        for r, row in enumerate(rows):
            if all(seg_end <= s or seg_start >= e for s, e, _ in row):
                row.append((seg_start, seg_end, label))
                row_index = r
                break
        else:
            rows.append([(seg_start, seg_end, label)])
            row_index = len(rows) - 1

        color = "#%06x" % random.randint(0, 0xFFFFFF)
        base_y = freq_line_y_coordinates[line_index]
        y1 = base_y - 30 - row_index * (row_height + 4)
        y2 = y1 + row_height

        x1 = freqToPixelX(seg_start, min_f, max_f)
        x2 = freqToPixelX(seg_end, min_f, max_f)
        x1 = max(margin, min(canvas_width - margin, x1))
        x2 = max(margin, min(canvas_width - margin, x2))

        c.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        rect_width = x2 - x1
        approx_text_width = len(label) * 6  # ca 6 pixlar per tecken vid font storlek 6


        if rect_width*1.9 >= approx_text_width:
            c.create_text((x1 + x2)/2, (y1 + y2)/2, text=label, font=("Ericsson Hilda", 6), anchor="c")

    
root.mainloop() # start loop



