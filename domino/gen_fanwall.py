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

n_spokes = 5
per_spoke = 20
total = n_spokes * per_spoke

domino_list = []
count = 0

domino_list.append(f'    <body pos="0 0 {dzz:.4f}" euler="0 0 0">')
domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="1.0 0.2 0.2 1"/>')
domino_list.append(f'      <freejoint/>')
domino_list.append(f'    </body>')
count += 1

for si in range(n_spokes):
    angle_deg = si * (360.0 / n_spokes)
    theta = np.radians(angle_deg)

    spoke_len = per_spoke * 1.4
    t_fine = np.linspace(0, spoke_len, per_spoke * 100)
    px = t_fine * np.cos(theta)
    py = t_fine * np.sin(theta)

    ds = np.sqrt(np.gradient(px)**2 + np.gradient(py)**2)
    L = np.cumsum(ds)
    Ls = np.linspace(0, L[-1], per_spoke)

    px_f = np.interp(Ls, L, px)
    py_f = np.interp(Ls, L, py)

    angles = np.arctan2(np.gradient(px_f), np.gradient(py_f))

    hue_base = si / n_spokes

    for di in range(per_spoke):
        hue = (hue_base + di * 0.01) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        ad = np.degrees(angles[di]) + 90
        tilt_y = 5 if (si == 0 and di == 0) else 0

        domino_list.append(f'    <body pos="{px_f[di]:.4f} {py_f[di]:.4f} {dzz:.4f}" euler="0 {tilt_y:.1f} {ad:.1f}">')
        domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{r:.3f} {g:.3f} {b:.3f} 1"/>')
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

with open("domino/fanwall.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote fanwall.xml ({count} blocks)")
