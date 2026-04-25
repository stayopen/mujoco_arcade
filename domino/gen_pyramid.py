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

BW = 0.025
BH = 0.012
GAP = 0.003
SPACING = 2 * BW + GAP

layer_counts = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

domino_list = []
count = 0
z = BH

for li, n in enumerate(layer_counts):
    if count + n > 295:
        break
    if li == 0:
        bl = (n - 1) * SPACING / 2 + BW
    else:
        prev_n = layer_counts[li - 1]
        bl = (prev_n - 1) * SPACING / 2 + BW

    hue = 0.02 + li * 0.07
    r, g, b = colorsys.hsv_to_rgb(hue % 1.0, 0.85, 0.92)

    for i in range(n):
        offset = (i - (n - 1) / 2.0) * SPACING
        if li % 2 == 0:
            pos = f"0 {offset:.4f} {z:.4f}"
            size = f"{bl:.4f} {BW:.4f} {BH:.4f}"
        else:
            pos = f"{offset:.4f} 0 {z:.4f}"
            size = f"{BW:.4f} {bl:.4f} {BH:.4f}"

        domino_list.append(f'    <body pos="{pos}">')
        domino_list.append(f'      <geom type="box" size="{size}" rgba="{r:.3f} {g:.3f} {b:.3f} 1"/>')
        domino_list.append(f'      <freejoint/>')
        domino_list.append(f'    </body>')
        count += 1

    z += 2 * BH

bodies_xml = "\n".join(domino_list)
xml = f"""{HEADER}  <worldbody>
    <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>
{bodies_xml}
  </worldbody>
</mujoco>
"""

with open("domino/pyramid.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote pyramid.xml ({count} blocks)")
