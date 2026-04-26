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

# Concentric rings with varying density
rings = [
    (1.0, 8),
    (1.8, 12),
    (2.6, 16),
    (3.4, 20),
    (4.2, 24),
    (5.0, 28),
]

for ring_idx, (radius, n_dom) in enumerate(rings):
    angles = np.linspace(0, 2*np.pi, n_dom, endpoint=False)
    for i, a in enumerate(angles):
        px = radius * np.cos(a)
        py = radius * np.sin(a)
        # Tangent to circle
        angle = a + np.pi/2
        hue = (ring_idx + i/n_dom) / len(rings)
        c = colorsys.hsv_to_rgb(hue % 1.0, 0.9, 0.95)
        is_first = (count == 0)
        tilt_y = 15 if is_first else 0
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

with open("domino/mandala.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote mandala.xml ({count} blocks)")
