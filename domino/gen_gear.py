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

n_teeth = 10
inner_r = 2.5
outer_r = 3.8
tooth_width = 0.4

domino_list = []
count = 0

for i in range(n_teeth):
    base_angle = i * (2 * np.pi / n_teeth)
    # Tooth is a line from inner_r to outer_r, angled slightly
    n_seg = max(2, int((outer_r - inner_r) / 0.5))
    for k in range(n_seg):
        t = k / n_seg
        r = inner_r + t * (outer_r - inner_r)
        angle = base_angle
        px = r * np.cos(angle)
        py = r * np.sin(angle)
        is_first = (count == 0)
        tilt_y = 10 if is_first else 0
        hue = i / n_teeth
        c = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        domino_list.append(f'    <body pos="{px:.4f} {py:.4f} {dzz:.4f}" euler="0 {tilt_y:.1f} {np.degrees(angle + np.pi/2):.1f}">')
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

with open("domino/gear.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote gear.xml ({count} blocks)")
