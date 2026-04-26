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

n_petals = 6
petal_len = 3.5
petal_arc = np.pi / 4

domino_list = []
count = 0

for p in range(n_petals):
    base_angle = p * (2 * np.pi / n_petals)
    t = np.linspace(0, 1, 5000)
    # Start from r=0.6 (not 0) to avoid center overlap
    r = 1.0 + petal_len * t
    arc = petal_arc * (t - 0.5)
    angle = base_angle + arc
    px = r * np.cos(angle)
    py = r * np.sin(angle)
    
    # Distance-aware sampling
    min_dist = 0.70
    kept_x = [px[0]]
    kept_y = [py[0]]
    for i in range(1, len(px)):
        if np.hypot(px[i]-kept_x[-1], py[i]-kept_y[-1]) >= min_dist:
            kept_x.append(px[i])
            kept_y.append(py[i])
        if len(kept_x) >= 50:
            break
    
    px_f = np.array(kept_x)
    py_f = np.array(kept_y)
    angles = np.arctan2(np.gradient(py_f), np.gradient(px_f))
    hue = p / n_petals
    c = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    
    for i in range(len(px_f)):
        is_first = (count == 0)
        tilt_y = 10 if is_first else 0
        domino_list.append(f'    <body pos="{px_f[i]:.4f} {py_f[i]:.4f} {dzz:.4f}" euler="0 {tilt_y:.1f} {np.degrees(angles[i]):.1f}">')
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

with open("domino/flower.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote flower.xml ({count} blocks)")
