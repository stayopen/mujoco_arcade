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
dz = 10
scale = 0.1
dxx = dx * scale
dyy = dy * scale
dzz = dz * scale

N = 280
initial_radius = 2
n_turns = 5
final_radius = 10

b = (final_radius - initial_radius) / (2 * np.pi * n_turns)
start_theta = np.pi / 2
end_theta = 2 * np.pi * n_turns

s = np.linspace(start_theta, end_theta, N * 10)
x = (initial_radius + b * s) * np.cos(s)
y = (initial_radius + b * s) * np.sin(s)

ds = np.sqrt(np.gradient(x)**2 + np.gradient(y)**2)
L = np.cumsum(ds)
Ls = np.linspace(0, L[-1], N)

new_s = np.interp(Ls, L, s)
x = (initial_radius + b * new_s) * np.cos(new_s)
y = (initial_radius + b * new_s) * np.sin(new_s)

hues = np.linspace(0, 1, N, endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

domino_list = []
count = 0

for i in range(N):
    c = colors[i]
    euler_z = new_s[i] * 180 / np.pi + 90
    euler_x = -5 if i == 0 else 0

    domino_list.append(f'    <body pos="{x[i]:.4f} {y[i]:.4f} {dzz:.4f}" euler="{euler_x:.1f} 0 {euler_z:.1f}">')
    domino_list.append(f'      <geom type="box" size="{dxx} {dyy} {dzz}" rgba="{c[0]:.3f} {c[1]:.3f} {c[2]:.3f} 1"/>')
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

with open("domino/spiralwall.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote spiralwall.xml ({count} blocks)")
