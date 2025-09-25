# --- Imports ---
import json
import tkinter as tk
import math
import random

# --- Canvas setup ---
canvas_width = 1500
canvas_height = 1080
margin = 80
row_height = 18
freq_line_y_coordinates = [200, 400, 600, 800]
freq_line_width = 2

# --- Frequency ranges for the new zoomed-in four lines ---
line_ranges = {
    0: {"min": 0, "max": 12.20703125},
    1: {"min": 12.20703125, "max": 24.4140625},
    2: {"min": 24.4140625, "max": 36.62109375},
    3: {"min": 36.62109375, "max": 48.828125},
}

# --- Custom tick positions for each line ---
line_ticks_custom = {
    0: [0, 0.009, 0.07, 0.4, 9.9],     # ticks for line 0
    1: [13.2, 15.1, 18.9, 24],            # ticks for line 1
    2: [25.55, 28, 31.375, 35.275],            # ticks for line 2
    3: [38.25, 39.55, 41.015, 48.828125]          # ticks for line 3 
    # the last box keeps going so the last tick is just where the logarithmic line stops
}

# --- Load data ---
with open("data.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

# --- Filter and convert bands ---
bands = []
for b in raw:
    start = float(b["startfrekvens"])
    end = float(b["slutfrekvens"])
    label = b["användningsområde"]
    if end > start and end >= 0 and start <= 48.828125:
        start = max(start, 0)
        end = min(end, 48.828125)
        bands.append((start, end, label))

# --- Tkinter setup ---
root = tk.Tk()
root.title("Frequency Allocation 0-48.828125 MHz")
c = tk.Canvas(root, width=canvas_width, height=canvas_height, background="white")
c.pack()

# --- Functions ---
def freqToPixelX(freq, min_f, max_f):
    log_min = math.log10(max(min_f, 1e-6))  # avoid log(0)
    log_max = math.log10(max_f)
    log_freq = math.log10(max(freq, 1e-6))
    pixel_x = margin + (log_freq - log_min) / (log_max - log_min) * (canvas_width - 2 * margin)
    return pixel_x

def draw_custom_ticks_log(y, line_index, min_f, max_f):
    """Draw user-defined ticks on a logarithmic axis."""
    ticks = line_ticks_custom.get(line_index, [])
    for tick in ticks:
        if min_f <= tick <= max_f:
            x = freqToPixelX(tick, min_f, max_f)
            c.create_line(x, y - 5, x, y + 5)
            c.create_text(x, y + 15, text=f"{tick:.6f} MHz", font=("Arial", 7))

# --- Draw lines and ticks ---
for line_index, y in enumerate(freq_line_y_coordinates):
    min_f = line_ranges[line_index]["min"]
    max_f = line_ranges[line_index]["max"]

    # Draw horizontal line
    c.create_line(margin, y, canvas_width - margin, y, width=freq_line_width)

    # Draw ticks
    draw_custom_ticks_log(y, line_index, min_f, max_f)

# --- Draw bands ---
rows_per_line = [[] for _ in range(len(freq_line_y_coordinates))]

for start, end, label in bands:
    for line_index in range(len(freq_line_y_coordinates)):
        min_f = line_ranges[line_index]["min"]
        max_f = line_ranges[line_index]["max"]
        seg_start = max(start, min_f)
        seg_end = min(end, max_f)
        if seg_end <= seg_start:
            continue

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
        if x2 - x1 > 30:
            c.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=label, font=("Arial", 6))

root.mainloop()