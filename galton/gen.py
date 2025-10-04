
import numpy as np
pin_list = []

z = 0
dz = 0.1
r = 0.03
for i in range(17):
    
    for y_pos in np.arange(-2.7, 2.71, .2):
        pin = f"""<body pos=".2 {y_pos} {4.5+z}" euler="0 90 0">
                <geom type="cylinder" size="{r} .1" rgba="0.4 .9 0.9 1"/>
        </body>"""
        pin_list.append(pin)
    z += dz
    for y_pos in np.arange(-2.6, 2.61, .2):
        pin = f"""<body pos=".2 {y_pos} {4.5+z}" euler="0 90 0">
                <geom type="cylinder" size="{r} .1" rgba="0.4 .9 0.9 1"/>
        </body>"""
        pin_list.append(pin)
    z += dz

for y_pos in np.arange(-2.7, 2.71, .2):
    pin = f"""<body pos=".2 {y_pos} {4.5+z}" euler="0 90 0">
            <geom type="cylinder" size="{r} .1" rgba="0.4 .9 0.9 1"/>
    </body>"""
    pin_list.append(pin)

pin_xml = "\n".join(pin_list)

# create balls
bin_width=.2


ball_list = []
for b_xpos in np.arange(-2.01,2.01,0.1):
    for b_zpos in np.arange(0, 1, 0.1):
        ball = f""" <body pos=".2 {b_xpos} {13.6 + b_zpos}">
	          <freejoint />
			  <geom type="sphere" size=".01" rgba="1 0. 0 1"/>
	  </body>"""
        ball_list.append(ball)

balls_xml = "\n".join(ball_list)


sep_list = []
for y_pos in np.arange(-2.7, 2.71, .1):
    sep = f"""<body  pos=".2 {y_pos} 2">
			  <geom type="box" size=".1 .01 2" rgba="0.4 .9 09 1"/>
		  </body> """
    sep_list.append(sep)
sep_xml = "\n".join(sep_list)


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
      <body name="backboard" pos="0 0 5.5">
			  <geom type="box" size=".1 3 5.5" rgba="0 .9 0 1	"/>
	  </body>
      <body name="frontboard" pos="0.4 0 5.5">
			  <geom type="box" size=".1 3 5.5" rgba="0 .9 09 .1"/>
	  </body>

      <body name="left_column" pos=".2 -2.95 4">
			  <geom type="box" size=".1 .01 4" rgba="0.4 .9 09 .1"/>
		  </body>
      <body name="right_column" pos=".2 2.95 4">
			  <geom type="box" size=".1 .01 4" rgba="0.4 .9 09 1"/>
		  </body>

      <body name="left_ball_ramp" pos=".2 -1.75 9" euler="85 0 0">
			  <geom type="box" size=".12 .05 1.72" rgba="0.4 .9 09 1"/>
	  </body>

      <body name="right_ball_ramp" pos=".2 1.75 9" euler="-85 0 0">
			  <geom type="box" size=".12 .05 1.72    " rgba="0.4 .9 09 1"/>
	  </body>

      <body name="left_ball_ramp3" pos=".2 -1.75 10.5" euler="75 0 0">
			  <geom type="box" size=".12 .05 1.72" rgba="0.4 .9 09 1"/>
	  </body>

      <body name="right_ball_ramp3" pos=".2 1.75 10.5" euler="-75 0 0">
			  <geom type="box" size=".12 .05 1.72    " rgba="0.4 .9 09 1"/>
              
	  </body>
      
      {balls_xml}
      {pin_xml}
      {sep_xml}
  </worldbody>
</mujoco>
"""

 
with open("galton/galton1.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print("Wrote galton1.xml")
