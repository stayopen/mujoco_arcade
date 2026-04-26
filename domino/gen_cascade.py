import numpy as np
import colorsys
from domino_util import write_path_xml

t = np.linspace(0, 3, 100000)
px = 8 * np.sin(2 * np.pi * t / 3)
py = t * 30

ds = np.sqrt(np.gradient(px)**2 + np.gradient(py)**2)
L = np.cumsum(ds)
total_length = L[-1]

N = min(int(total_length / 0.38), 300)
Ls = np.linspace(0, L[-1], N)
px_f = np.interp(Ls, L, px)
py_f = np.interp(Ls, L, py)

hues = np.linspace(0, 1, N, endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/cascade.xml", px_f, py_f, colors=colors)
