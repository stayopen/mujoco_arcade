import numpy as np
import colorsys
from domino_util import write_path_xml

n_petals = 6
inner_r = 1.5
petal_len = 3.0

t = np.linspace(0, 1.85 * np.pi, 120000)
r = inner_r + petal_len * (0.5 + 0.5 * np.sin(n_petals * t))
px = r * np.cos(t)
py = r * np.sin(t)

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/flower.xml", px, py, colors=colors, chain_spacing=0.75)
