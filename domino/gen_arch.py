import numpy as np
import colorsys
from domino_util import write_path_xml

arch_r = 5.0
start_angle = np.pi * 0.05
end_angle = np.pi * 0.95
t = np.linspace(start_angle, end_angle, 50000)
px = arch_r * np.cos(t)
py = arch_r * np.sin(t)

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/arch.xml", px, py, colors=colors, min_dist=0.80)
