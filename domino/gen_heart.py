import numpy as np
import colorsys
from domino_util import write_path_xml

t = np.linspace(0, 2 * np.pi, 200000)
hx = 16 * np.sin(t)**3
hy = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
scale_factor = 0.12
px = hx * scale_factor
py = hy * scale_factor

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/heart.xml", px, py, colors=colors)
