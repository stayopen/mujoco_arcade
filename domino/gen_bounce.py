import numpy as np
import colorsys
from domino_util import write_path_xml

xlim, ylim = 4.0, 3.0
x, y = 0.0, 0.0
vx, vy = 0.35, 0.22
dt = 0.05
points = [(x, y)]
for _ in range(2000):
    x += vx * dt
    y += vy * dt
    if abs(x) > xlim:
        vx = -vx
        x = np.sign(x) * xlim
    if abs(y) > ylim:
        vy = -vy
        y = np.sign(y) * ylim
    points.append((x, y))

px = np.array([p[0] for p in points])
py = np.array([p[1] for p in points])

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/bounce.xml", px, py, colors=colors)
