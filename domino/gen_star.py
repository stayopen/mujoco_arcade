import numpy as np
import colorsys
from domino_util import write_path_xml

n_points = 5
outer_r = 5.5
inner_r = 2.6

angles_outer = np.linspace(np.pi/2, np.pi/2 + 2*np.pi, n_points, endpoint=False)
angles_inner = angles_outer + np.pi / n_points

path_points = []
for i in range(n_points):
    path_points.append((outer_r*np.cos(angles_outer[i]), outer_r*np.sin(angles_outer[i])))
    path_points.append((inner_r*np.cos(angles_inner[i]), inner_r*np.sin(angles_inner[i])))
path_points.append(path_points[0])

t_fine = np.linspace(0, len(path_points)-1, 200000)
px = np.interp(t_fine, range(len(path_points)), [p[0] for p in path_points])
py = np.interp(t_fine, range(len(path_points)), [p[1] for p in path_points])

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/star.xml", px, py, colors=colors)
