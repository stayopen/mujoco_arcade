import numpy as np
import colorsys

layer = 10
dx = 1
dy = 3
dz = 6
scale = 0.1

N = layer
domino_list = []
height = 0
for i in range(N, 0, -1):
    dxx = dx * scale
    dyy = dy * scale
    dzz = dz * scale
    color1 = (144 / 255., 213 / 255., 1)
    color2 = (255 / 255., 213 / 255., 133 / 255.)

    x_offset = 0
    for j in range(i):
        domino = f"""
        <body pos="{x_offset + dzz - dxx} 0 {dzz + height}" euler="0 0 0" >
         <geom type="box" size="{dxx} {dyy}  {dzz}" rgba="{color1[0]} {color1[1]} {color1[2]} 1"/>
         <freejoint/>
        </body>
        <body pos="{-(x_offset + dzz - dxx)} 0 {dzz + height}" euler="0 0 0" >
         <geom type="box" size="{dxx} {dyy}  {dzz}" rgba="{color1[0]} {color1[1]} {color1[2]} 1"/>
         <freejoint/>
        </body>
        
        
        """
        domino_list.append(domino)
        if i == N:
            if x_offset == 0:
                domino = f"""
                <body pos="{x_offset} 0 {dzz + height}" euler="0 0 0" >
                <geom type="box" size="{dxx} {dyy}  {dzz}" rgba="{color1[0]} {color1[1]} {color1[2]} 1"/>
                <freejoint/>
                </body>"""
            else:
                domino = f"""
                <body pos="{x_offset} 0 {dzz + height}" euler="0 0 0" >
                <geom type="box" size="{dxx} {dyy}  {dzz}" rgba="{color1[0]} {color1[1]} {color1[2]} 1"/>
                <freejoint/>
                </body>
                <body pos="{-x_offset} 0 {dzz + height}" euler="0 0 0" >
                <geom type="box" size="{dxx} {dyy}  {dzz}" rgba="{color1[0]} {color1[1]} {color1[2]} 1"/>
                <freejoint/>
                </body>
                            
                
                """
            domino_list.append(domino)

        x_offset = x_offset + (2*dzz - 2*dxx)

    x_offset = - x_offset + 2*dzz - 2*dxx
    for j in range(i):
        domino = f"""
         <body pos="{x_offset} 0 {height + 2*dzz + dxx}" euler="0 90 0" >
         <geom type="box" size="{dxx} {dyy}  {dzz}" rgba="{color2[0]} {color2[1]} {color2[2]} 1"/>
         <freejoint/>
        </body>
        
        """
        domino_list.append(domino)
        x_offset = x_offset + 4 * dzz - 4*dxx

    height += 2*dzz + 2*dxx

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

with open("domino/speedwall.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print("Write speedwall.xml")
