import numpy as np
import colorsys
from domino_util import write_path_xml

def dragon_curve(n_iter):
    s = "FX"
    for _ in range(n_iter):
        new_s = ""
        for ch in s:
            if ch == "X":
                new_s += "X+YF"
            elif ch == "Y":
                new_s += "FX-Y"
            else:
                new_s += ch
        s = new_s
    return s

s = dragon_curve(10)
x, y = 0.0, 0.0
angle = 0
points = [(x, y)]
step = 0.25

for ch in s:
    if ch == "F":
        x += step * np.cos(angle)
        y += step * np.sin(angle)
        points.append((x, y))
    elif ch == "+":
        angle += np.pi / 2
    elif ch == "-":
        angle -= np.pi / 2

px = np.array([p[0] for p in points])
py = np.array([p[1] for p in points])
px -= np.mean(px)
py -= np.mean(py)
max_r = max(np.max(np.abs(px)), np.max(np.abs(py)))
scale_f = 4.0 / max_r if max_r > 0 else 1.0
px *= scale_f
py *= scale_f

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/dragon.xml", px, py, colors=colors)
