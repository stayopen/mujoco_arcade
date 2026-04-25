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

dx = 1
dy = 3
dz = 6
scale = 0.1
dxx = dx * scale
dyy = dy * scale
dzz = dz * scale

N = 10
domino_list = []
count = 0

x_offset = 0.0

for peak_idx in range(3):
    peak_hue = peak_idx * 0.3
    height = 0

    for layer_i in range(N, 0, -1):
        if count > 295:
            break

        c1 = colorsys.hsv_to_rgb((peak_hue + layer_i * 0.04) % 1.0, 0.9, 0.95)
        c2 = colorsys.hsv_to_rgb((peak_hue + 0.15 + layer_i * 0.04) % 1.0, 0.7, 0.85)

        xp = x_offset
        for j in range(layer_i):
            is_first = (peak_idx == 0 and layer_i == N and j == 0)
            tilt_y = 5 if is_first else 0

            domino_list.append(f'    <body pos="{xp + dzz - dxx:.4f} 0 {dzz + height:.4f}" euler="0 {tilt_y} 0">')
            domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{c1[0]:.3f} {c1[1]:.3f} {c1[2]:.3f} 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            count += 1

            if not is_first:
                domino_list.append(f'    <body pos="{-(xp + dzz - dxx):.4f} 0 {dzz + height:.4f}" euler="0 0 0">')
                domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{c1[0]:.3f} {c1[1]:.3f} {c1[2]:.3f} 1"/>')
                domino_list.append(f'      <freejoint/>')
                domino_list.append(f'    </body>')
                count += 1

            xp += (2 * dzz - 2 * dxx)

        bx_offset = -xp + (2 * dzz - 2 * dxx)
        bx = bx_offset
        for j in range(layer_i):
            domino_list.append(f'    <body pos="{bx:.4f} 0 {height + 2 * dzz + dxx:.4f}" euler="0 90 0">')
            domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{c2[0]:.3f} {c2[1]:.3f} {c2[2]:.3f} 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            count += 1
            bx += 4 * dzz - 4 * dxx

        height += 2 * dzz + 2 * dxx

    x_offset += (N + 1) * (2 * dzz - 2 * dxx) + 0.5

bodies_xml = "\n".join(domino_list)
xml = f"""{HEADER}  <worldbody>
    <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>
{bodies_xml}
  </worldbody>
</mujoco>
"""

with open("domino/dualpeaks.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote dualpeaks.xml ({count} blocks)")
