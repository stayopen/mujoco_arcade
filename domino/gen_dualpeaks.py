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
dxx = round(dx * scale, 4)
dyy = round(dy * scale, 4)
dzz = round(dz * scale, 4)

step = 2 * dzz - 2 * dxx
cross_step = 4 * dzz - 4 * dxx

N = 8
# Space peaks so they don't overlap (each peak spans ~N*step + dzz on each side)
peak_spacing = 2 * N * step + 2.0

domino_list = []
count = 0

for peak_idx in range(2):
    cx = (peak_idx - 0.5) * peak_spacing
    hue_base = peak_idx * 0.3
    height = 0

    for layer_i in range(N, 0, -1):
        if count > 400:
            break

        c1 = colorsys.hsv_to_rgb((hue_base + (N - layer_i) * 0.04) % 1.0, 0.9, 0.95)
        c2 = colorsys.hsv_to_rgb((hue_base + 0.15 + (N - layer_i) * 0.04) % 1.0, 0.7, 0.85)

        # Vertical pillars
        x_offset = 0
        for j in range(layer_i):
            px = cx + x_offset + dzz - dxx

            domino_list.append(f'    <body pos="{px:.4f} 0 {dzz + height:.4f}" euler="0 0 0">')
            domino_list.append(f'      <geom type="box" size="{dxx:.4f} {dyy:.4f} {dzz:.4f}" rgba="{c1[0]:.3f} {c1[1]:.3f} {c1[2]:.3f} 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            count += 1

            domino_list.append(f'    <body pos="{cx - (x_offset + dzz - dxx):.4f} 0 {dzz + height:.4f}" euler="0 0 0">')
            domino_list.append(f'      <geom type="box" size="{dxx:.4f} {dyy:.4f} {dzz:.4f}" rgba="{c1[0]:.3f} {c1[1]:.3f} {c1[2]:.3f} 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            count += 1

            x_offset += step

        # Cross pieces on top of this layer
        bx = cx - x_offset + step
        for j in range(layer_i):
            is_top_peak0 = (peak_idx == 0 and layer_i == 1 and j == 0)
            tilt_cross = 10 if is_top_peak0 else 0
            z_offset = 0.15 if is_top_peak0 else 0.0
            domino_list.append(f'    <body pos="{bx:.4f} 0 {height + 2 * dzz + dxx + z_offset:.4f}" euler="0 {90 + tilt_cross:.1f} 0">')
            domino_list.append(f'      <geom type="box" size="{dxx:.4f} {dyy:.4f} {dzz:.4f}" rgba="{c2[0]:.3f} {c2[1]:.3f} {c2[2]:.3f} 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            count += 1
            bx += cross_step

        height += 2 * dzz + 2 * dxx

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
