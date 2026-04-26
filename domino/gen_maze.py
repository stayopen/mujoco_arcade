import numpy as np
import colorsys
from domino_util import write_path_xml

# Trace a path through a simple maze
maze = [
    "1111111111",
    "1000000001",
    "1011101111",
    "1010000001",
    "1010111011",
    "1000100001",
    "1110101111",
    "1000000001",
    "1011111101",
    "1000000001",
    "1111111111",
]
rows, cols = len(maze), len(maze[0])
cell = 0.45

# Find a Hamiltonian-like path through open cells (0s)
open_cells = [(r, c) for r in range(rows) for c in range(cols) if maze[r][c] == '0']

# Simple snake path through open cells
path = []
for r in range(rows):
    row_cells = [c for c in range(cols) if maze[r][c] == '0']
    if not row_cells:
        continue
    if r % 2 == 0:
        row_cells = sorted(row_cells)
    else:
        row_cells = sorted(row_cells, reverse=True)
    for c in row_cells:
        path.append((r, c))

px = np.array([(c - cols/2) * cell for r, c in path])
py = np.array([(rows/2 - r) * cell for r, c in path])

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/maze.xml", px, py, colors=colors)
