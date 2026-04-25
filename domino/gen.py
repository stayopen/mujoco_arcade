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

dz = 0
body_xml_list = []
for i in range(3):
    dy = 0.05

    pillar_xs = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    cross_xs = [".095", ".30", ".50", ".70", ".905"]
    cross_sizes = [".105", ".10", ".10", ".10", ".105"]

    for x in pillar_xs:
        sz = "0.1" if x == 0 else ".1"
        body_xml_list.append(f'    <body pos="{x} 0 {dz + .1}">')
        body_xml_list.append(f'      <freejoint/>')
        body_xml_list.append(f'      <geom type="box" size=".01 {dy} {sz}" rgba="0.4 .9 09 1"/>')
        body_xml_list.append(f'    </body>')

    for x, sz in zip(cross_xs, cross_sizes):
        body_xml_list.append(f'    <body pos="{x} 0 {dz + .21}">')
        body_xml_list.append(f'      <freejoint/>')
        body_xml_list.append(f'      <geom type="box" size="{sz} {dy} .01" rgba="0.9 .4 09 1"/>')
        body_xml_list.append(f'    </body>')

    dz += 0.22

bodies_xml = "\n".join(body_xml_list)

xml = f"""{HEADER}  <worldbody>
    <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>
{bodies_xml}
  </worldbody>
</mujoco>
"""

with open("domino/domino_tower.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print("Wrote domino_tower.xml")
