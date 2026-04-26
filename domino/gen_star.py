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

n_points = 5
outer_r = 5.5
inner_r = 2.8
gap = 0.52  # gap from vertices

domino_list = []
count = 0

# Build star segments: outer -> inner -> outer -> inner ...
angles_outer = np.linspace(np.pi/2, np.pi/2 + 2*np.pi, n_points, endpoint=False)
angles_inner = angles_outer + np.pi / n_points

all_segments = []
for i in range(n_points):
    a_out = angles_outer[i]
    a_in = angles_inner[i]
    a_out_next = angles_outer[(i+1) % n_points]
    
    # Segment from outer to inner
    x1, y1 = outer_r*np.cos(a_out), outer_r*np.sin(a_out)
    x2, y2 = inner_r*np.cos(a_in), inner_r*np.sin(a_in)
    all_segments.append((x1, y1, x2, y2))
    
    # Segment from inner to next outer
    x3, y3 = outer_r*np.cos(a_out_next), outer_r*np.sin(a_out_next)
    all_segments.append((x2, y2, x3, y3))

# Place dominoes along each segment, skipping gaps near endpoints
for seg_idx, (x1, y1, x2, y2) in enumerate(all_segments):
    seg_len = np.hypot(x2-x1, y2-y1)
    # Skip gap at both ends
    eff_len = seg_len - 2*gap
    if eff_len <= 0:
        continue
    
    angle = np.arctan2(y2-y1, x2-x1)
    n_seg = max(1, int(eff_len / 0.5))
    
    # Start after gap from (x1,y1)
    ux, uy = (x2-x1)/seg_len, (y2-y1)/seg_len
    for k in range(n_seg):
        t = gap + (k + 0.5) * eff_len / n_seg
        if t > seg_len - gap:
            break
        px = x1 + ux * t
        py = y1 + uy * t
        is_first = (count == 0)
        tilt_y = 10 if is_first else 0
        hue = seg_idx / len(all_segments)
        c = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
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

with open("domino/star.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote star.xml ({count} blocks)")
