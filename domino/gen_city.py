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

# City skyline: grid of buildings with varying heights
np.random.seed(42)
grid_w, grid_h = 6, 5
spacing = 1.2

domino_list = []
count = 0

for row in range(grid_h):
    for col in range(grid_w):
        px = (col - grid_w/2) * spacing
        py = (row - grid_h/2) * spacing
        # Height varies like a city skyline
        height_mult = 1.0 + 2.0 * np.sin(col * 0.7) * np.cos(row * 0.5)
        height_mult = max(0.5, height_mult)
        b_dzz = dzz * height_mult
        b_dzz = min(b_dzz, 2.0)  # cap height
        hue = (col + row) / (grid_w + grid_h)
        c = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
        is_first = (count == 0)
        tilt_y = 15 if is_first else 0
        domino_list.append(f'    <body pos="{px:.4f} {py:.4f} {b_dzz:.4f}" euler="0 {tilt_y:.1f} 0">')
        domino_list.append(f'      <geom type="box" size="{dxx:.4f} {dyy:.4f} {b_dzz:.4f}" rgba="{c[0]:.3f} {c[1]:.3f} {c[2]:.3f} 1"/>')
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

with open("domino/city.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote city.xml ({count} blocks)")
