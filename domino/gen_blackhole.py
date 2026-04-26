import numpy as np
import colorsys
from domino_util import write_path_xml

theta = np.linspace(0, 6 * np.pi, 200000)
a = 0.6
b = 0.13
r = a * np.exp(b * theta)
px = r * np.cos(theta)
py = r * np.sin(theta)

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/blackhole.xml", px, py, colors=colors, chain_spacing=0.75)
