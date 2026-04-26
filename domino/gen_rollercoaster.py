import numpy as np
import colorsys
from domino_util import write_path_xml

t = np.linspace(0, 10 * np.pi, 100000)
px = 0.22 * t
py = 1.5 * np.sin(0.4 * t)
pz = 0.6 + 0.5 * (1 + np.sin(0.3 * t))

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/rollercoaster.xml", px, py, pz, colors=colors)
