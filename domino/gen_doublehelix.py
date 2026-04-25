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

BL = 0.14
BW = 0.022
BH = 0.014

domino_list = []
count = 0

n_layers = 40
angle_per_layer = 9.0
dz_step = 2 * BH

for li in range(n_layers):
    z = BH + li * dz_step
    angle = li * angle_per_layer
    hue = li / n_layers
    r, g, b = colorsys.hsv_to_rgb(hue, 0.85, 0.95)

    for di in range(2):
        a = angle + di * 90
        r2, g2, b2 = colorsys.hsv_to_rgb((hue + di * 0.4) % 1.0, 0.85, 0.95)
        domino_list.append(f'    <body pos="0 0 {z:.4f}" euler="0 0 {a:.1f}">')
        domino_list.append(f'      <geom type="box" size="{BL:.4f} {BW:.4f} {BH:.4f}" rgba="{r2:.3f} {g2:.3f} {b2:.3f} 1"/>')
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

with open("domino/doublehelix.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote doublehelix.xml ({count} blocks)")
