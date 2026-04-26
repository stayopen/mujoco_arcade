import numpy as np
import colorsys
from domino_util import write_path_xml

n_spokes = 5
per_spoke = 20
spoke_len = per_spoke * 0.38 + 2 * 0.3

px_all = []
py_all = []
colors_all = []

count = 0
for si in range(n_spokes):
    angle_deg = si * (360.0 / n_spokes)
    theta = np.radians(angle_deg)
    t_fine = np.linspace(0.9, spoke_len, per_spoke * 100)
    px = t_fine * np.cos(theta)
    py = t_fine * np.sin(theta)
    
    ds = np.sqrt(np.gradient(px)**2 + np.gradient(py)**2)
    L = np.cumsum(ds)
    Ls = np.linspace(0, L[-1], per_spoke)
    px_f = np.interp(Ls, L, px)
    py_f = np.interp(Ls, L, py)
    
    hue_base = si / n_spokes
    for di in range(per_spoke):
        hue = (hue_base + di * 0.01) % 1.0
        c = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        px_all.append(px_f[di])
        py_all.append(py_f[di])
        colors_all.append(c)
        count += 1
        if count >= 300:
            break
    if count >= 300:
        break

write_path_xml("domino/fanwall.xml", px_all, py_all, colors=colors_all)
