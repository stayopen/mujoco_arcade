import numpy as np
import colorsys
from domino_util import write_path_xml

n_petals = 6
petal_len = 3.5
petal_arc = np.pi / 4

px_all = []
py_all = []
colors_all = []

for p in range(n_petals):
    base_angle = p * (2 * np.pi / n_petals)
    t = np.linspace(0, 1, 5000)
    r = 1.0 + petal_len * t
    arc = petal_arc * (t - 0.5)
    angle = base_angle + arc
    px = r * np.cos(angle)
    py = r * np.sin(angle)
    
    hue = p / n_petals
    c = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    for i in range(len(px)):
        px_all.append(px[i])
        py_all.append(py[i])
        colors_all.append(c)

write_path_xml("domino/flower.xml", px_all, py_all, colors=colors_all)
