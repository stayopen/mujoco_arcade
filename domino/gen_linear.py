
import numpy as np
import colorsys

pin_list = []

N = 50
dx = 0.2
dy = 3
dz = 6

start  = 1
end = 100
ratios = np.logspace(np.log10(start), np.log10(end), N)
scale = 0.01
hues = np.linspace(0, 1, N, endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

domino_list = []
y = 0
for i in range(N):
    dxx = dx * ratios[i] * scale
    dyy = dy * ratios[i] * scale
    dzz = dz * ratios[i] * scale 
    c = colors[i]
    euler_x = 0
    if i == 0:
        euler_x = -5
    domino = f"""<body pos="0 {y+dyy} {dzz}" euler="{euler_x} 0 0" >
         <geom type="box" size="{dyy} {dxx}  {dzz}" rgba="{c[0]} {c[1]} {c[2]} 1"/>
         <freejoint/>
        </body>"""
    domino_list.append(domino)
    y+= 2* dyy
 

 

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

 
with open("domino/domino1.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print("Wrote domino1.xml")
