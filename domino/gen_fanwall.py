import numpy as np
import colorsys
from domino_util import write_path_xml

n_spokes = 5
inner_r = 0.9
outer_r = 4.0

px_all = []
py_all = []

for si in range(n_spokes):
    theta0 = si * (2 * np.pi / n_spokes)
    theta1 = (si + 1) * (2 * np.pi / n_spokes)
    radius = np.linspace(inner_r, outer_r, 500)
    if si % 2 == 1:
        radius = radius[::-1]
    px_all.extend(radius * np.cos(theta0))
    py_all.extend(radius * np.sin(theta0))

    arc_r = radius[-1]
    theta = np.linspace(theta0, theta1, 500)
    px_all.extend(arc_r * np.cos(theta))
    py_all.extend(arc_r * np.sin(theta))

px = np.array(px_all)
py = np.array(py_all)
hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/fanwall.xml", px, py, colors=colors, chain_spacing=0.75)
