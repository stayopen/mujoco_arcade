import numpy as np
import colorsys
from domino_util import write_path_xml

# Winding path that goes up one peak and down the other
n = 200000
t = np.linspace(0, 1, n)
px = 8 * (t - 0.5)
py = 2.0 * np.sin(4 * np.pi * t) + 0.5 * np.sin(12 * np.pi * t)

hues = np.linspace(0, 1, n, endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

# Keep the chain on the floor; floating blocks fall before the trigger reaches them.
write_path_xml("domino/dualpeaks.xml", px, py, colors=colors, chain_spacing=0.75)
