
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


bodies_xml = "\n".join(body_layers)


xml = f"""<mujoco>
<!-- <option gravity="0 0 0" /> -->
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
{bodies_xml}
</worldbody>
</mujoco>"""

 
with open("domino/domino_tower.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print("Wrote domino_tower.xml")
