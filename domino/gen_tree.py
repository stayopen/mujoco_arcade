import numpy as np
import colorsys
from domino_util import write_path_xml

# A meandering path that looks like a tree trunk and branches
t = np.linspace(0, 4 * np.pi, 100000)
px = 0.5 * t + 0.8 * np.sin(2 * t)
py = 3.0 * np.sin(0.5 * t) + 0.5 * np.cos(3 * t)

# Center vertically
py -= np.mean(py)

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 0.7, 0.9) for h in hues]

write_path_xml("domino/tree.xml", px, py, colors=colors)
