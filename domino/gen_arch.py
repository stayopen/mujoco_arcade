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

# Arch bridge: semicircle with a small gap at top
arch_r = 3.0
start_angle = np.pi * 0.05
end_angle = np.pi * 0.95
t = np.linspace(start_angle, end_angle, 50000)

px = arch_r * np.cos(t)
py = arch_r * np.sin(t)

# Arch rises from floor, so z increases with y
# We'll make dominoes stand on the floor and lean to form an arch
# Actually, place them along the semicircle in x-y, each standing upright on the floor
# But z should follow the arch height? No, for a ground-level arch, just place them on floor.
# To make it look like an arch, place them along the semicircle.

ds = np.sqrt(np.gradient(px)**2 + np.gradient(py)**2)
L = np.cumsum(ds)
total_length = L[-1]

target_spacing = 0.42
N = min(int(total_length / target_spacing), 300)

Ls = np.linspace(0, L[-1], N)
px_f = np.interp(Ls, L, px)
py_f = np.interp(Ls, L, py)

# Tangent angle along the arch
angles = np.arctan2(np.gradient(py_f), np.gradient(px_f))

hues = np.linspace(0, 1, N, endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

domino_list = []
count = 0

for i in range(N):
    c = colors[i]
    euler_z = np.degrees(angles[i])
    tilt_y = 15 if i == 0 else 0
    domino_list.append(f'    <body pos="{px_f[i]:.4f} {py_f[i]:.4f} {dzz:.4f}" euler="0 {tilt_y:.1f} {euler_z:.1f}">')
    domino_list.append(f'      <geom type="box" size="{dxx:.4f} {dyy:.4f} {dzz:.4f}" rgba="{c[0]:.3f} {c[1]:.3f} {c[2]:.3f} 1"/>')
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

with open("domino/arch.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote arch.xml ({count} blocks)")
