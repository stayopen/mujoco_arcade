import numpy as np
import colorsys
from domino_util import write_path_xml

# Serpentine path through a grid
rows, cols = 8, 10
spacing = 0.80
px_all = []
py_all = []

for r in range(rows):
    for c in range(cols):
        if r % 2 == 0:
            x = c * spacing
        else:
            x = (cols - 1 - c) * spacing
        y = r * spacing
        px_all.append(x)
        py_all.append(y)

px = np.array(px_all) - (cols - 1) * spacing / 2
py = np.array(py_all) - (rows - 1) * spacing / 2

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 0.8, 0.95) for h in hues]

write_path_xml("domino/wavegrid.xml", px, py, colors=colors, chain_spacing=0.75)
