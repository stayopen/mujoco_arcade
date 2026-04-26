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

# Grid of dominoes where each row is offset sinusoidally
nx = 15
ny = 12
spacing_x = 0.55
spacing_y = 0.7

domino_list = []
count = 0

for j in range(ny):
    for i in range(nx):
        px = (i - nx/2) * spacing_x
        py = (j - ny/2) * spacing_y + 0.3 * np.sin(i * 0.8)
        # Tangent angle follows the wave slope
        angle = np.arctan2(0.3 * 0.8 * np.cos(i * 0.8), spacing_x)
        hue = (i + j) / (nx + ny)
        c = colorsys.hsv_to_rgb(hue, 0.8, 0.95)
        is_first = (count == 0)
        tilt_y = 10 if is_first else 0
        domino_list.append(f'    <body pos="{px:.4f} {py:.4f} {dzz:.4f}" euler="0 {tilt_y:.1f} {np.degrees(angle):.1f}">')
        domino_list.append(f'      <geom type="box" size="{dxx:.4f} {dyy:.4f} {dzz:.4f}" rgba="{c[0]:.3f} {c[1]:.3f} {c[2]:.3f} 1"/>')
        domino_list.append(f'      <freejoint/>')
        domino_list.append(f'    </body>')
        count += 1
        if count >= 300:
            break
    if count >= 300:
        break

bodies_xml = "\n".join(domino_list)
xml = f"""{HEADER}  <worldbody>
    <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>
{bodies_xml}
  </worldbody>
</mujoco>
"""

with open("domino/wavegrid.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote wavegrid.xml ({count} blocks)")
