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
dz = 6
scale = 0.1
dxx = round(dx * scale, 4)
dyy = round(dy * scale, 4)
dzz = round(dz * scale, 4)

t = np.linspace(0, 8 * np.pi, 200000)
px = 0.12 * t + 1.2 * np.sin(t)
py = 1.8 * np.sin(0.7 * t) + 0.6 * np.cos(1.3 * t)

# Distance-aware sampling
min_dist = 0.65
kept_x = [px[0]]
kept_y = [py[0]]
for i in range(1, len(px)):
    dx_i = px[i] - np.array(kept_x)
    dy_i = py[i] - np.array(kept_y)
    if np.min(np.hypot(dx_i, dy_i)) >= min_dist:
        kept_x.append(px[i])
        kept_y.append(py[i])
    if len(kept_x) >= 300:
        break

px_f = np.array(kept_x)
py_f = np.array(kept_y)
N = len(px_f)
angles = np.arctan2(np.gradient(py_f), np.gradient(px_f))
hues = np.linspace(0, 1, N, endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

domino_list = []
count = 0
for i in range(N):
    c = colors[i]
    euler_z = np.degrees(angles[i])
    tilt_y = 15 if i == 0 else 0
    domino_list.append(f'    <body pos="{px_f[i]:.4f} {py_f[i]:.4f} {dzz:.4f}" euler="0 {tilt_y:.1f} {euler_z:.1f}">')
    domino_list.append(f'      <geom type="box" size="{dxx:.4f} {dyy:.4f} {dzz:.4f}" rgba="{c[0]:.3f} {c[1]:.3f} {c[2]:.3f} 1"/>')
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

with open("domino/snake.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote snake.xml ({count} blocks)")
