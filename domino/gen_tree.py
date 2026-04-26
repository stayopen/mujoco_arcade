import numpy as np
import colorsys
from domino_util import write_path_xml

# A meandering path that looks like a tree trunk and branches
t = np.linspace(0, 1, 100000)
px = 9.0 * (t - 0.5)
py = 2.5 * np.sin(2 * np.pi * t) + 0.8 * np.sin(6 * np.pi * t)

# Center vertically
py -= np.mean(py)
px *= 1.35
py *= 1.35

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 0.7, 0.9) for h in hues]

write_path_xml("domino/tree.xml", px, py, colors=colors, chain_spacing=0.75)
