
import numpy as np
import colorsys


layer = 20
dx = 1
dy = 3
dz = 6

scale = 0.1

 
 

domino_list = []

for i in range(N):
    dxx = dx * scale
    dyy = dy * scale
    dzz = dz * scale
    color1 = (0.9, 0, 0)
    color2 = (0, 0.9, 0)
   
    if i == N-1:
        euler_x = 25
    domino = f"""    <body pos="{x[i]} {y[i]} {dzz}" euler="{euler_x} 0 {new_s[i]* 180/np.pi + 90}" >
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
 
      
{"\n".join(domino_list)}
  </worldbody>
</mujoco>
"""

 
with open("domino/domino2.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print("Wrote domino2.xml")
