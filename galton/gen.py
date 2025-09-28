
dz = 0
body_layers = []
for i in range(3):

    dy =0.05
    body_layer=f"""<body pos="0 0 {dz + .1}">
    <freejoint />
            <geom type="box" size=".01 {dy} 0.1" rgba="0.4 .9 09 1"/>
        </body>
    <body pos="0.2 0 {dz + .1}">
    <freejoint />
            <geom type="box" size=".01 {dy} .1" rgba="0.4 .9 09 1"/>
        </body>
    <body  pos="0.4 0 {dz + .1}">
    <freejoint />
        <geom type="box" size=".01 {dy} .1" rgba="0.4 .9 09 1"/>
        </body>
    <body  pos="0.6 0 {dz + .1}">
    <freejoint />
        <geom type="box" size=".01 {dy} .1" rgba="0.4 .9 09 1"/>
        </body>
    <body  pos="0.8 0 {dz + .1}">
    <freejoint />
        <geom type="box" size=".01 {dy} .1" rgba="0.4 .9 09 1"/>
        </body>
    <body  pos="1.0 0 {dz + .1}">
    <freejoint />
        <geom type="box" size=".01 {dy} .1" rgba="0.4 .9 09 1"/>
        </body>


    <body  pos=".095 0 {dz + .21}">
    <freejoint />
        <geom type="box" size=".105 {dy} .01" rgba="0.9 .4 09 1"/>
        </body>
    <body  pos=".30 0 {dz + .21}">
    <freejoint />
        <geom type="box" size=".10 {dy} .01" rgba="0.9 .4 09 1"/>
    </body>
    <body  pos=".50 0 {dz + .21}">
    <freejoint />
        <geom type="box" size=".10 {dy} .01" rgba="0.9 .4 09 1"/>
    </body>
    <body  pos=".70 0 {dz + .21}">
    <freejoint />
        <geom type="box" size=".10 {dy} .01" rgba="0.9 .4 09 1"/>
    </body>
    <body  pos=".905 0 {dz + .21}">
    <freejoint />
        <geom type="box" size=".105 {dy} .01" rgba="0.9 .4 09 1"/>
    </body>"""

    dz = dz + 0.22
    body_layers.append(body_layer)

	balls = """ <body pos=".2 2 12">
	          <freejoint />
			  <geom type="sphere" size=".05" rgba="1 0. 0 1"/>
	  </body>
	  <body pos=".2 -2 12">
	          <freejoint />
			  <geom type="sphere" size=".05" rgba="1 0. 0 1"/>
	  </body>"""
bodies_xml = "\n".join(body_layers)


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
			  <geom type="box" size=".1 3 5.5" rgba="0 .9 0 .3	"/>
	  </body>
      <body name="frontboard" pos="0.4 0 5.5">
			  <geom type="box" size=".1 3 5.5" rgba="0 .9 09 .25"/>
	  </body>

      <body name="left_column" pos=".2 -2.95 4">
			  <geom type="box" size=".1 .01 4" rgba="0.4 .9 09 1"/>
		  </body>
      <body name="right_column" pos=".2 2.95 4">
			  <geom type="box" size=".1 .01 4" rgba="0.4 .9 09 1"/>
		  </body>

      <body name="left_ball_ramp" pos=".2 -1.75 10" euler="40 0 0">
			  <geom type="box" size=".1 .01 2.6" rgba="0.4 .9 09 1"/>
	  </body>

      <body name="right_ball_ramp" pos=".2 1.75 10" euler="-40 0 0">
			  <geom type="box" size=".1 .01 2.6" rgba="0.4 .9 09 1"/>
	  </body>



      <body  pos=".2 -2.75 2">
			  <geom type="box" size=".1 .01 2" rgba="0.4 .9 09 1"/>
		  </body>
      <body pos=".2 -2.55 2">
			  <geom type="box" size=".1 .01 2" rgba="0.4 .9 09 1"/>
		  </body>

      <body  pos=".2 -2.35 2">
			  <geom type="box" size=".1 .01 2" rgba="0.4 .9 09 1"/>
		  </body>
      <body pos=".2 -2.15 2">
			  <geom type="box" size=".1 .01 2" rgba="0.4 .9 09 1"/>
		  </body>

      <body  pos=".2 -1.95 2">
			  <geom type="box" size=".1 .01 2" rgba="0.4 .9 09 1"/>
		  </body>
      <body pos=".2 -1.75 2">
			  <geom type="box" size=".1 .01 2" rgba="0.4 .9 09 1"/>
		  </body>

      <body  pos=".2 -2.75 2">
			  <geom type="box" size=".1 .01 2" rgba="0.4 .9 09 1"/>
		  </body>
      <body pos=".2 -2.55 2">
			  <geom type="box" size=".1 .01 2" rgba="0.4 .9 09 1"/>
		  </body>

      <body  pos=".2 -2.75 2">
			  <geom type="box" size=".1 .01 2" rgba="0.4 .9 09 1"/>
		  </body>
      <body pos=".2 -2.55 2">
			  <geom type="box" size=".1 .01 2" rgba="0.4 .9 09 1"/>
		  </body>

      <body  pos=".2 -2.75 2">
			  <geom type="box" size=".1 .01 2" rgba="0.4 .9 09 1"/>
		  </body>
      <body pos=".2 -2.55 2">
			  <geom type="box" size=".1 .01 2" rgba="0.4 .9 09 1"/>
	  </body>
	  <body pos=".2 -2.55 4.5" euler="0 90 0">
			  <geom type="cylinder" size=".05 .1" rgba="0.4 .9 0.9 1"/>
	  </body>

  </worldbody>
</mujoco>
"""

 
with open("galton/galton1.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print("Wrote galton1.xml")
