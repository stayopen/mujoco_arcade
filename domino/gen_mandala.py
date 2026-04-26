import numpy as np
import colorsys
from domino_util import write_path_xml

# Archimedean spiral from outside to inside
t = np.linspace(6 * np.pi, 0, 100000)
a = 0.15
b = 0.25
r = a + b * t
px = r * np.cos(t)
py = r * np.sin(t)

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/mandala.xml", px, py, colors=colors, chain_spacing=0.75)
