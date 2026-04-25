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
chain_spacing = 2 * dyy + 0.04
TILT = -8

domino_list = []
count = 0

segments = 8
per_segment = 12

cx, cy = 0.0, 0.0
current_dir = 0

for seg_idx in range(segments):
    dir_rad = np.radians(current_dir)
    step_x = chain_spacing * np.sin(dir_rad)
    step_y = chain_spacing * np.cos(dir_rad)

    for di in range(per_segment):
        if count > 298:
            break

        hue = (seg_idx + di / per_segment) / segments
        r, g, b = colorsys.hsv_to_rgb(hue % 1.0, 0.85, 0.92)
        is_first = (seg_idx == 0 and di == 0)
        tilt_x = TILT if is_first else 0

        domino_list.append(f'    <body pos="{cx:.4f} {cy:.4f} {dzz:.4f}" euler="{tilt_x} 0 {current_dir:.1f}">')
        domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{r:.3f} {g:.3f} {b:.3f} 1"/>')
        domino_list.append(f'      <freejoint/>')
        domino_list.append(f'    </body>')
        count += 1

        cx += step_x
        cy += step_y

    current_dir += 90

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
