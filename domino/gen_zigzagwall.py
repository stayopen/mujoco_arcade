import numpy as np
import colorsys

HEADER = """<mujoco>
  <visual>
    <headlight diffuse="0.6 0.6 0.6" ambient="0.1 0.1 0.1" specular="0 0 0"/>
    <rgba haze="0.15 0.25 0.35 1"/>
    <global azimuth="120" elevation="-20"/>
  </visual>
  <asset>
    <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0 0 0" width="512" height="3072"/>
    <texture type="2d" name="groundplane" builtin="checker" mark="edge" rgb1="0.2 0.3 0.4" rgb2="0.1 0.2 0.3" markrgb="0.8 0.8 0.8" width="300" height="300"/>
    <material name="groundplane" texture="groundplane" texuniform="true" texrepeat="5 5" reflectance="0.2"/>
  </asset>
"""

dx = 1
dy = 3
dz = 10
scale = 0.1
dxx = dx * scale
dyy = dy * scale
dzz = dz * scale

N = 200
seg_len = 5.0
n_segs = 8

pts_x = [0.0]
pts_y = [0.0]
angle = 0.0

for s in range(n_segs):
    angle += np.pi / 2
    pts_x.append(pts_x[-1] + seg_len * np.sin(angle))
    pts_y.append(pts_y[-1] + seg_len * np.cos(angle))

waypoints = list(zip(pts_x, pts_y))

all_px, all_py = [], []
for i in range(len(waypoints) - 1):
    x0, y0 = waypoints[i]
    x1, y1 = waypoints[i + 1]
    n_pts = 500
    for j in range(n_pts):
        t = j / n_pts
        all_px.append(x0 + t * (x1 - x0))
        all_py.append(y0 + t * (y1 - y0))

all_px = np.array(all_px)
all_py = np.array(all_py)

ds = np.sqrt(np.gradient(all_px)**2 + np.gradient(all_py)**2)
L = np.cumsum(ds)
Ls = np.linspace(0, L[-1], N)

px_f = np.interp(Ls, L, all_px)
py_f = np.interp(Ls, L, all_py)

angles = np.arctan2(np.gradient(px_f), np.gradient(py_f))

hues = np.linspace(0, 1, N, endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

domino_list = []
count = 0

for i in range(N):
    c = colors[i]
    ad = np.degrees(angles[i]) + 90
    tilt_y = 5 if i == 0 else 0

    domino_list.append(f'    <body pos="{px_f[i]:.4f} {py_f[i]:.4f} {dzz:.4f}" euler="0 {tilt_y:.1f} {ad:.1f}">')
    domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{c[0]:.3f} {c[1]:.3f} {c[2]:.3f} 1"/>')
    domino_list.append(f'      <freejoint/>')
    domino_list.append(f'    </body>')
    count += 1

bodies_xml = "\n".join(domino_list)
xml = f"""{HEADER}  <worldbody>
    <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>
{bodies_xml}
  </worldbody>
</mujoco>
"""

with open("domino/zigzagwall.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote zigzagwall.xml ({count} blocks)")
