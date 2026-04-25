import numpy as np
import colorsys

layer = 20
dx = 1
dy = 6
dz = 3
scale = 0.1

N = layer
domino_list = []
height = 0
for i in range(N):
    dxx = dx * scale
    dyy = dy * scale
    dzz = dz * scale
    color1 = (144 / 255., 213 / 255., 1)

    domino_list.append(f'    <body pos="0 0 {dzz + height}" euler="0 0 0">')
    domino_list.append(f'      <geom type="box" size="{dxx} {dyy}  {dzz}" rgba="{color1[0]} {color1[1]} {color1[2]} 1"/>')
    domino_list.append(f'      <freejoint/>')
    domino_list.append(f'    </body>')
    domino_list.append(f'    <body pos="{2*dyy - 2*dxx} 0 {dzz + height}" euler="0 0 0">')
    domino_list.append(f'      <geom type="box" size="{dxx} {dyy}  {dzz}" rgba="{color1[0]} {color1[1]} {color1[2]} 1"/>')
    domino_list.append(f'      <freejoint/>')
    domino_list.append(f'    </body>')
    domino_list.append(f'    <body pos="{dyy - dxx} {dyy - dxx} {3*dzz + height}" euler="0 0 90">')
    domino_list.append(f'      <geom type="box" size="{dxx} {dyy}  {dzz}" rgba="{color1[0]} {color1[1]} {color1[2]} 1"/>')
    domino_list.append(f'      <freejoint/>')
    domino_list.append(f'    </body>')
    domino_list.append(f'    <body pos="{dyy - dxx} {dxx- dyy} {3*dzz + height}" euler="0 0 90">')
    domino_list.append(f'      <geom type="box" size="{dxx} {dyy}  {dzz}" rgba="{color1[0]} {color1[1]} {color1[2]} 1"/>')
    domino_list.append(f'      <freejoint/>')
    domino_list.append(f'    </body>')

    height += 4 * dzz

bodies_xml = "\n".join(domino_list)

xml = f"""<mujoco>
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
  <worldbody>
    <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>
{bodies_xml}
  </worldbody>
</mujoco>
"""

with open("domino/domino1x1tower.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print("Wrote domino1x1tower.xml")
