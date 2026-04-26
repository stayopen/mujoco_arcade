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

domino_list = []
count = 0

# Use a list of all placed positions for overlap checking
placed = []

def can_place(px, py, angle):
    global placed
    # Check against all previously placed dominoes
    for (ox, oy, oa) in placed:
        # Simple center distance check; domino width ~0.6
        if np.hypot(px-ox, py-oy) < 0.55:
            return False
    return True

def branch(px, py, angle, length, depth, max_depth):
    global count, placed
    if count >= 300:
        return
    n = max(2, int(length / 0.5))
    for i in range(n):
        if count >= 300:
            return
        t = (i + 1) / n
        bx = px + length * t * np.cos(angle)
        by = py + length * t * np.sin(angle)
        if not can_place(bx, by, angle):
            continue
        is_first = (count == 0)
        tilt_y = 10 if is_first else 0
        hue = depth / max_depth
        c = colorsys.hsv_to_rgb(hue, 0.7 + 0.3*(1-depth/max_depth), 0.9)
        domino_list.append(f'    <body pos="{bx:.4f} {by:.4f} {dzz:.4f}" euler="0 {tilt_y:.1f} {np.degrees(angle):.1f}">')
        domino_list.append(f'      <geom type="box" size="{dxx:.4f} {dyy:.4f} {dzz:.4f}" rgba="{c[0]:.3f} {c[1]:.3f} {c[2]:.3f} 1"/>')
        domino_list.append(f'      <freejoint/>')
        domino_list.append(f'    </body>')
        placed.append((bx, by, angle))
        count += 1
    
    if depth < max_depth:
        end_x = px + length * np.cos(angle)
        end_y = py + length * np.sin(angle)
        new_len = length * 0.65
        branch(end_x, end_y, angle + np.pi/5, new_len, depth+1, max_depth)
        branch(end_x, end_y, angle - np.pi/5, new_len, depth+1, max_depth)

branch(0, -3.0, np.pi/2, 2.5, 0, 4)

bodies_xml = "\n".join(domino_list)
xml = f"""{HEADER}  <worldbody>
    <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>
{bodies_xml}
  </worldbody>
</mujoco>
"""

with open("domino/tree.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote tree.xml ({count} blocks)")
