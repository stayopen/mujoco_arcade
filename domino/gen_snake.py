import numpy as np
import colorsys
from domino_util import write_path_xml

t = np.linspace(0, 8 * np.pi, 200000)
px = 0.12 * t + 1.2 * np.sin(t)
py = 1.8 * np.sin(0.7 * t) + 0.6 * np.cos(1.3 * t)

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/snake.xml", px, py, colors=colors)
