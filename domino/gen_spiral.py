
import numpy as np
import colorsys

pin_list = []

N = 200
dx = 1
dy = 3
dz = 10

scale = 0.1

hues = np.linspace(0, 1, N, endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

initial_radius = 2
n_turns = 5
final_radius = 10

b = (final_radius - initial_radius)/(2*np.pi*n_turns)

start_theta = np.pi/2
end_theta = 2*np.pi*n_turns

s = np.linspace(start_theta, end_theta, N)
x = (initial_radius + b*s)*np.cos(s)
y = (initial_radius + b*s)*np.sin(s)

# Calculate the arc length
L = np.cumsum(np.sqrt(np.gradient(x)**2 + np.gradient(y)**2))
Ls = np.linspace(0, L[-1], N)

# Find s values for equally spaced arc lengths
new_s = np.interp(Ls, L, s)

# Calculate x and y for equally spaced arc lengths
x = (initial_radius + b*new_s)*np.cos(new_s)
y = (initial_radius + b*new_s)*np.sin(new_s)

 


domino_list = []

for i in range(N):
    dxx = dx * scale
    dyy = dy * scale
    dzz = dz * scale
    c = colors[i]
    euler_x = 0
    if i == N-1:
        euler_x = 25
    domino = f"""<body pos="{x[i]} {y[i]} {dzz}" euler="{euler_x} 0 {new_s[i]* 180/np.pi + 90}" >
         <geom type="box" size="{dxx} {dyy}  {dzz}" rgba="{c[0]} {c[1]} {c[2]} 1"/>
         <freejoint/>
        </body>"""
    domino_list.append(domino)
 

 

xml = f"""<mujoco>
  <visual>
    <headlight diffuse="0.6 0.6 0.6" ambient="0.1 0.1 0.1" specular="0 0 0"/>
    <rgba haze="0.15 0.25 0.35 1"/>
    <global azimuth="120" elevation="-20"/>
  </visual>

  <asset>
    <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0 0 0" width="512" height="3072"/>
    <texture type="2d" name="groundplane" builtin="checker" mark="edge" rgb1="0.2 0.3 0.4" rgb2="0.1 0.2 0.3"
      markrgb="0.8 0.8 0.8" width="300" height="300"/>
    <material name="groundplane" texture="groundplane" texuniform="true" texrepeat="5 5" reflectance="0.2"/>
  </asset>

  <worldbody>
    <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>
 
      
      {domino_list}
  </worldbody>
</mujoco>
"""

 
with open("domino/domino2.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print("Wrote domino2.xml")
