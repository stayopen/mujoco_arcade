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

domino_list = []
count = 0

peak_sizes = [7, 5, 8]
x_offset = 0.0

for pi, peak_n in enumerate(peak_sizes):
    peak_hue = pi * 0.3
    height = 0

    for layer_i in range(peak_n, 0, -1):
        if count > 295:
            break

        n_dom = layer_i
        c1 = colorsys.hsv_to_rgb((peak_hue + layer_i * 0.05) % 1.0, 0.9, 0.95)
        c2 = colorsys.hsv_to_rgb((peak_hue + 0.15 + layer_i * 0.05) % 1.0, 0.7, 0.85)

        dx_pos = x_offset
        for j in range(n_dom):
            domino_list.append(f'    <body pos="{dx_pos + dzz - dxx:.4f} 0 {dzz + height:.4f}" euler="0 0 0">')
            domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{c1[0]:.3f} {c1[1]:.3f} {c1[2]:.3f} 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            count += 1

            if layer_i == peak_sizes[pi] and j == 0 and pi == 0 and layer_i == peak_n:
                pass
            elif n_dom > 1 or j > 0:
                domino_list.append(f'    <body pos="{-(dx_pos + dzz - dxx):.4f} 0 {dzz + height:.4f}" euler="0 0 0">')
                domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{c1[0]:.3f} {c1[1]:.3f} {c1[2]:.3f} 1"/>')
                domino_list.append(f'      <freejoint/>')
                domino_list.append(f'    </body>')
                count += 1

            dx_pos += (2 * dzz - 2 * dxx)

        if layer_i == peak_n and pi == 0:
            domino_list.append(f'    <body pos="0 0 {dzz + height:.4f}" euler="0 {-8} 0">')
            domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="1.0 0.15 0.15 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            count += 1

        bx_offset = -(dx_pos - (2 * dzz - 2 * dxx)) + 2 * dzz - 2 * dxx
        bx_pos = bx_offset
        for j in range(layer_i):
            domino_list.append(f'    <body pos="{bx_pos:.4f} 0 {height + 2 * dzz + dxx:.4f}" euler="0 90 0">')
            domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{c2[0]:.3f} {c2[1]:.3f} {c2[2]:.3f} 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            count += 1
            bx_pos += 4 * dzz - 4 * dxx

        height += 2 * dzz + 2 * dxx

    x_offset += (peak_n + 1) * (2 * dzz - 2 * dxx) + 0.3

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
