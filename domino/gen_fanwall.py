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

n_spokes = 7
dominoes_per_spoke = 14
radius_start = chain_spacing

hue_idx = 0
total = n_spokes * dominoes_per_spoke + 1

for si in range(n_spokes):
    angle_deg = si * (360.0 / n_spokes)
    theta = np.radians(angle_deg)
    hue_base = si / n_spokes

    for di in range(dominoes_per_spoke):
        t = radius_start + di * chain_spacing
        x = t * np.cos(theta)
        y = t * np.sin(theta)
        euler_z = angle_deg + 90

        hue = hue_base + di * 0.02
        r, g, b = colorsys.hsv_to_rgb(hue % 1.0, 0.9, 0.95)

        is_first = (si == 0 and di == 0)
        tilt_x = TILT if is_first else 0

        domino_list.append(f'    <body pos="{x:.4f} {y:.4f} {dzz:.4f}" euler="{tilt_x} 0 {euler_z:.1f}">')
        domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{r:.3f} {g:.3f} {b:.3f} 1"/>')
        domino_list.append(f'      <freejoint/>')
        domino_list.append(f'    </body>')
        count += 1

        if count > 298:
            break
    if count > 298:
        break

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
