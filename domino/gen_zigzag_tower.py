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

BL = 0.12
BW = 0.025
BH = 0.015

domino_list = []
count = 0

n_layers = 24
overhang = 0.008
dz_step = 2 * BH

x_off = 0.0
y_off = 0.0

for li in range(n_layers):
    z = BH + li * dz_step
    hue = li / n_layers
    r, g, b = colorsys.hsv_to_rgb(hue, 0.85, 0.95)

    period = 6
    phase = li % (2 * period)
    if phase < period:
        x_off += overhang
    else:
        x_off -= overhang

    if (li // (2 * period)) % 2 == 1:
        y_off += overhang if phase < period else -overhang

    for di in range(2):
        y = (di - 0.5) * (2 * BW + 0.004)
        if li % 2 == 0:
            pos = f"{x_off:.4f} {y:.4f} {z:.4f}"
            size = f"{BL:.4f} {BW:.4f} {BH:.4f}"
        else:
            pos = f"{y:.4f} {x_off:.4f} {z:.4f}"
            size = f"{BW:.4f} {BL:.4f} {BH:.4f}"

        domino_list.append(f'    <body pos="{pos}">')
        domino_list.append(f'      <geom type="box" size="{size}" rgba="{r:.3f} {g:.3f} {b:.3f} 1"/>')
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

with open("domino/zigzag_tower.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote zigzag_tower.xml ({count} blocks)")
