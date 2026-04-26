import numpy as np
import colorsys
from domino_util import write_path_xml

n_teeth = 10
inner_r = 2.5
outer_r = 3.8

t = np.linspace(0, 2 * np.pi, 100000)
# Gear profile: radius oscillates between inner and outer
r = (inner_r + outer_r) / 2 + (outer_r - inner_r) / 2 * np.sign(np.sin(n_teeth * t))
# Smooth it slightly
r = (inner_r + outer_r) / 2 + (outer_r - inner_r) / 2 * np.tanh(5 * np.sin(n_teeth * t))
px = r * np.cos(t)
py = r * np.sin(t)

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/gear.xml", px, py, colors=colors)
