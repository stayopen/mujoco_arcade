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
dyy = 0.04
dzz = 0.06
dz_step = 2 * dzz

domino_list = []
count = 0

outer_n = 24
outer_radius = 0.30
outer_layers = 8

arch_positions = {0, 6, 12, 18}
arch_skip_layers = {2, 3, 4}

for li in range(outer_layers):
    z = dzz + li * dz_step
    for i in range(outer_n):
        if i in arch_positions and li in arch_skip_layers:
            continue

        theta = 2 * np.pi * i / outer_n
        x = outer_radius * np.cos(theta)
        y = outer_radius * np.sin(theta)
        angle = np.degrees(theta) + 90

        hue = 0.06 + li * 0.10
        sat = 0.7 if i not in arch_positions else 0.9
        r, g, b = colorsys.hsv_to_rgb(hue % 1.0, sat, 0.90)
        domino_list.append(f'    <body pos="{x:.4f} {y:.4f} {z:.4f}" euler="0 0 {angle:.1f}">')
        domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{r:.3f} {g:.3f} {b:.3f} 1"/>')
        domino_list.append(f'      <freejoint/>')
        domino_list.append(f'    </body>')
        count += 1

    for ai in arch_positions:
        if li in arch_skip_layers and li + 1 == max(arch_skip_layers) + 1 - 1:
            pass
        if li == min(arch_skip_layers) - 1:
            theta1 = 2 * np.pi * ai / outer_n
            theta2 = 2 * np.pi * ((ai + 1) % outer_n) / outer_n
            theta_mid = (theta1 + theta2) / 2
            if ai == max(arch_positions):
                theta_mid = theta1 + np.pi / outer_n
            x1 = outer_radius * np.cos(theta1)
            y1 = outer_radius * np.sin(theta1)
            x2 = outer_radius * np.cos(theta2)
            y2 = outer_radius * np.sin(theta2)
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            mid_angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            z_cap = z + dzz + 0.005
            domino_list.append(f'    <body pos="{mx:.4f} {my:.4f} {z_cap:.4f}" euler="0 0 {mid_angle:.1f}">')
            domino_list.append(f'      <geom type="box" size="0.05 0.015 0.005" rgba="0.9 0.85 0.7 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            count += 1

inner_n = 12
inner_radius = 0.15
inner_layers = 4

for li in range(inner_layers):
    z = dzz + li * dz_step
    for i in range(inner_n):
        theta = 2 * np.pi * i / inner_n
        x = inner_radius * np.cos(theta)
        y = inner_radius * np.sin(theta)
        angle = np.degrees(theta) + 90

        hue = 0.55 + li * 0.08
        r, g, b = colorsys.hsv_to_rgb(hue % 1.0, 0.65, 0.88)
        domino_list.append(f'    <body pos="{x:.4f} {y:.4f} {z:.4f}" euler="0 0 {angle:.1f}">')
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

with open("domino/colosseum.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote colosseum.xml ({count} blocks)")
