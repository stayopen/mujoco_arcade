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

dxx = 0.05
dyy = 0.12
dzz = 0.25
row_gap = 0.15

domino_list = []
count = 0

max_per_row = 12
n_rows = 10
row_spacing = 2 * dzz + row_gap
bridge_spacing = 4 * dzz - 4 * dxx

trigger_y = -0.3
domino_list.append(f'    <body pos="0 {trigger_y:.4f} {dzz:.4f}" euler="0 0 -8">')
domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="1.0 0.2 0.2 1"/>')
domino_list.append(f'      <freejoint/>')
domino_list.append(f'    </body>')
count += 1

y = 0
for ri in range(n_rows):
    n_in_row = 2 + ri
    if n_in_row > max_per_row:
        n_in_row = max_per_row
    if count + n_in_row > 298:
        break

    hue = ri / n_rows
    c1 = colorsys.hsv_to_rgb(hue, 0.9, 0.95)
    c2 = colorsys.hsv_to_rgb((hue + 0.15) % 1.0, 0.7, 0.88)

    x_start = -(n_in_row - 1) * (2 * dyy + 0.02) / 2

    for di in range(n_in_row):
        x = x_start + di * (2 * dyy + 0.02)
        domino_list.append(f'    <body pos="{x:.4f} {y:.4f} {dzz:.4f}" euler="0 0 0">')
        domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{c1[0]:.3f} {c1[1]:.3f} {c1[2]:.3f} 1"/>')
        domino_list.append(f'      <freejoint/>')
        domino_list.append(f'    </body>')
        count += 1

    if ri < n_rows - 1:
        n_bridge = n_in_row
        x_start_b = -(n_bridge - 1) * (2 * dyy + 0.02) / 2
        bridge_y = y + dzz + dxx + 0.01

        for di in range(n_bridge):
            x = x_start_b + di * (2 * dyy + 0.02)
            domino_list.append(f'    <body pos="{x:.4f} {bridge_y:.4f} {dxx + 0.01:.4f}" euler="0 0 90">')
            domino_list.append(f'      <geom type="box" size="{dzz:.4f} {dyy:.4f} {dxx:.4f}" rgba="{c2[0]:.3f} {c2[1]:.3f} {c2[2]:.3f} 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            count += 1

    y += row_spacing

bodies_xml = "\n".join(domino_list)
xml = f"""{HEADER}  <worldbody>
    <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>
{bodies_xml}
  </worldbody>
</mujoco>
"""

with open("domino/cascade.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote cascade.xml ({count} blocks)")
