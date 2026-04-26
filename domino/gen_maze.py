import numpy as np
import colorsys
from domino_util import write_path_xml

# A continuous maze-like serpentine corridor.  The writer resamples this into
# evenly spaced blocks so every corner remains part of the same chain.
rows, cols = 7, 9
cell = 0.80

px_all = []
py_all = []
for r in range(rows):
    x_row = np.linspace(0, (cols - 1) * cell, 500)
    if r % 2 == 1:
        x_row = x_row[::-1]
    y_row = np.full_like(x_row, r * cell)
    px_all.extend(x_row)
    py_all.extend(y_row)

    if r < rows - 1:
        y_link = np.linspace(r * cell, (r + 1) * cell, 120)
        x_link = np.full_like(y_link, x_row[-1])
        px_all.extend(x_link)
        py_all.extend(y_link)

px = np.array(px_all) - (cols - 1) * cell / 2
py = np.array(py_all) - (rows - 1) * cell / 2

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/maze.xml", px, py, colors=colors, chain_spacing=0.75)
