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

dxx = 0.02
dyy = 0.05
dzz = 0.06
dz_step = 2 * dzz

domino_list = []
count = 0

n_columns = 3
n_layers = 25
radius = 0.04
angle_step = 15.0

for ci in range(n_columns):
    base_angle = ci * (360.0 / n_columns)
    theta_base = np.radians(base_angle)
    cx = radius * np.cos(theta_base)
    cy = radius * np.sin(theta_base)

    for li in range(n_layers):
        z = dzz + li * dz_step
        angle = base_angle + li * angle_step
        hue = (ci / n_columns + li / n_layers * 0.5) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 0.9, 0.95)

        domino_list.append(f'    <body pos="{cx:.4f} {cy:.4f} {z:.4f}" euler="0 0 {angle:.1f}">')
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

with open("domino/spiral_tower.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote spiral_tower.xml ({count} blocks)")
