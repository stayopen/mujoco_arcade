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
domino_spacing = 2 * dyy + 0.03
row_width = 8

domino_list = []
count = 0

segments = 8

cx, cy = 0.0, -0.5
current_dir = 0

domino_list.append(f'    <body pos="{cx:.4f} {cy:.4f} {dzz:.4f}" euler="0 0 -8">')
domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="1.0 0.15 0.15 1"/>')
domino_list.append(f'      <freejoint/>')
domino_list.append(f'    </body>')
count += 1

cy += domino_spacing

for seg_idx in range(segments):
    if count > 280:
        break

    n_dominoes = 12
    dir_angle = current_dir
    dir_rad = np.radians(dir_angle)
    step_x = domino_spacing * np.sin(dir_rad)
    step_y = domino_spacing * np.cos(dir_rad)

    hue = seg_idx / segments
    r, g, b = colorsys.hsv_to_rgb(hue, 0.85, 0.92)

    for di in range(n_dominoes):
        if count > 298:
            break

        domino_list.append(f'    <body pos="{cx:.4f} {cy:.4f} {dzz:.4f}" euler="0 0 {dir_angle:.1f}">')
        domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{r:.3f} {g:.3f} {b:.3f} 1"/>')
        domino_list.append(f'      <freejoint/>')
        domino_list.append(f'    </body>')
        count += 1

        cx += step_x
        cy += step_y

    corner_x = cx - step_x
    corner_y = cy - step_y

    current_dir += 90
    dir_rad = np.radians(current_dir)
    step_x = domino_spacing * np.sin(dir_rad)
    step_y = domino_spacing * np.cos(dir_rad)
    cx = corner_x + step_x
    cy = corner_y + step_y

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
