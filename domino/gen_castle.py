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
dyy = 0.05
dzz = 0.08
dz_step = 2 * dzz

domino_list = []
count = 0

tower_positions = [(-0.4, -0.4), (0.4, -0.4), (-0.4, 0.4), (0.4, 0.4)]
tower_layers = 10

for ti, (tx, ty) in enumerate(tower_positions):
    hue_base = ti * 0.22
    r, g, b = colorsys.hsv_to_rgb(hue_base, 0.75, 0.88)

    for layer in range(tower_layers):
        z = dzz + layer * dz_step
        if layer % 2 == 0:
            domino_list.append(f'    <body pos="{tx - dyy:.4f} {ty:.4f} {z:.4f}" euler="0 0 0">')
            domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{r:.3f} {g:.3f} {b:.3f} 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            domino_list.append(f'    <body pos="{tx + dyy:.4f} {ty:.4f} {z:.4f}" euler="0 0 0">')
            domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{r:.3f} {g:.3f} {b:.3f} 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            count += 2
        else:
            domino_list.append(f'    <body pos="{tx:.4f} {ty - dyy:.4f} {z:.4f}" euler="0 0 90">')
            domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{r:.3f} {g:.3f} {b:.3f} 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            domino_list.append(f'    <body pos="{tx:.4f} {ty + dyy:.4f} {z:.4f}" euler="0 0 90">')
            domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{r:.3f} {g:.3f} {b:.3f} 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            count += 2

    top_z = dzz + tower_layers * dz_step
    for dx_off in [-dyy, 0, dyy]:
        domino_list.append(f'    <body pos="{tx + dx_off:.4f} {ty:.4f} {top_z:.4f}" euler="0 0 90">')
        domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="0.85 0.15 0.15 1"/>')
        domino_list.append(f'      <freejoint/>')
        domino_list.append(f'    </body>')
        count += 1

wall_r, wall_g, wall_b = colorsys.hsv_to_rgb(0.08, 0.55, 0.82)
wall_n = 8
wall_x_span = tower_positions[1][0] - tower_positions[0][0]
wall_spacing = (wall_x_span - 2 * dyy) / (wall_n + 1)
wall_layers = 4

for side in range(4):
    for i in range(wall_n):
        t = (i + 1) * wall_spacing
        if side == 0:
            x = tower_positions[0][0] + dyy + t
            y = tower_positions[0][1]
        elif side == 1:
            x = tower_positions[2][0] + dyy + t
            y = tower_positions[2][1]
        elif side == 2:
            x = tower_positions[0][0]
            y = tower_positions[0][1] + dyy + t
        else:
            x = tower_positions[1][0]
            y = tower_positions[1][1] + dyy + t

        for wl in range(wall_layers):
            z = dzz + wl * dz_step
            if side < 2:
                euler = "0 0 0"
            else:
                euler = "0 0 90"

            domino_list.append(f'    <body pos="{x:.4f} {y:.4f} {z:.4f}" euler="{euler}">')
            domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{wall_r:.3f} {wall_g:.3f} {wall_b:.3f} 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            count += 1

        if count > 295:
            break
    if count > 295:
        break

bodies_xml = "\n".join(domino_list)
xml = f"""{HEADER}  <worldbody>
    <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>
{bodies_xml}
  </worldbody>
</mujoco>
"""

with open("domino/castle.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote castle.xml ({count} blocks)")
