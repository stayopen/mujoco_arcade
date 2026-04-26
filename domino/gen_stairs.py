import numpy as np
import colorsys
from domino_util import write_path_xml

n_steps = 40
step_dx = 0.38
px = np.arange(n_steps) * step_dx
py = np.zeros(n_steps)
pz = 0.6 + np.arange(n_steps) * 0.25

hues = np.linspace(0, 1, n_steps, endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/stairs.xml", px, py, pz, colors=colors)
