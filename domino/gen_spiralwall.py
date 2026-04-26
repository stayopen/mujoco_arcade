import numpy as np
import colorsys
from domino_util import write_path_xml

initial_radius = 3
n_turns = 2
final_radius = 14

b = (final_radius - initial_radius) / (2 * np.pi * n_turns)
start_theta = np.pi / 2
end_theta = 2 * np.pi * n_turns

s = np.linspace(start_theta, end_theta, 100000)
x = (initial_radius + b * s) * np.cos(s)
y = (initial_radius + b * s) * np.sin(s)

ds = np.sqrt(np.gradient(x)**2 + np.gradient(y)**2)
L = np.cumsum(ds)
total_length = L[-1]

N = min(int(total_length / 0.38), 300)
Ls = np.linspace(0, L[-1], N)
new_s = np.interp(Ls, L, s)
x = (initial_radius + b * new_s) * np.cos(new_s)
y = (initial_radius + b * new_s) * np.sin(new_s)

hues = np.linspace(0, 1, N, endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/spiralwall.xml", x, y, colors=colors)
