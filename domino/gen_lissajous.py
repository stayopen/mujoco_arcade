import numpy as np
import colorsys
from domino_util import write_path_xml

t = np.linspace(0, 2 * np.pi, 200000)
A, B = 3.0, 2.8
a, b = 3, 4
delta = np.pi / 2
px = A * np.sin(a * t + delta)
py = B * np.sin(b * t)

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/lissajous.xml", px, py, colors=colors)
