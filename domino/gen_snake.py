import numpy as np
import colorsys
from domino_util import write_path_xml

t = np.linspace(0, 1, 200000)
px = 10.0 * (t - 0.5)
py = 1.8 * np.sin(5 * np.pi * t) + 0.5 * np.sin(13 * np.pi * t)

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/snake.xml", px, py, colors=colors, chain_spacing=0.75)
