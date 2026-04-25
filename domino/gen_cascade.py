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
spacing = 2 * dzz - 2 * dxx
TILT = -8

domino_list = []
count = 0

N = 290
hues = np.linspace(0, 1, N, endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 0.9, 0.95) for h in hues]

y = dyy
for i in range(N):
    c = colors[i]
    ex = 0 if i > 0 else TILT
    domino_list.append(f'    <body pos="0 {y:.4f} {dzz:.4f}" euler="{ex} 0 0">')
    domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{c[0]:.3f} {c[1]:.3f} {c[2]:.3f} 1"/>')
    domino_list.append(f'      <freejoint/>')
    domino_list.append(f'    </body>')
    count += 1
    y += 2 * dyy + spacing * 0.15

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
