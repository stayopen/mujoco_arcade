HEADER = """<mujoco>
  <visual>
    <headlight diffuse="0.6 0.6 0.6" ambient="0.1 0.1 0.1" specular="0 0 0"/>
    <rgba haze="0.15 0.25 0.35 1"/>
    <global azimuth="130" elevation="-18"/>
  </visual>
  <asset>
    <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0 0 0" width="512" height="3072"/>
    <texture type="2d" name="groundplane" builtin="checker" mark="edge" rgb1="0.2 0.3 0.4" rgb2="0.1 0.2 0.3" markrgb="0.8 0.8 0.8" width="300" height="300"/>
    <material name="groundplane" texture="groundplane" texuniform="true" texrepeat="5 5" reflectance="0.2"/>
  </asset>
"""

# Bright toy-block colors, ordered to resemble the reference photo.
COLORS = [
    (0.95, 0.08, 0.48),  # magenta
    (0.05, 0.34, 0.88),  # blue
    (0.00, 0.58, 0.18),  # green
    (0.95, 0.78, 0.02),  # yellow
]

beam_len = 1.12
beam_w = 0.11
course_z = 0.11

x_cols = [-0.90, -0.30, 0.30, 0.90]
y_faces = [-0.62, 0.62]
layers = 32

domino_list = []
count = 0


def add_box(x, y, z, sx, sy, sz, color):
    global count
    domino_list.append(f'    <body pos="{x:.4f} {y:.4f} {z:.4f}" euler="0 0 0">')
    domino_list.append(
        f'      <geom type="box" size="{sx:.4f} {sy:.4f} {sz:.4f}" '
        f'rgba="{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} 1"/>'
    )
    domino_list.append('      <freejoint/>')
    domino_list.append('    </body>')
    count += 1


for layer in range(layers):
    color = COLORS[layer % len(COLORS)]
    z = course_z + layer * (2 * course_z)

    if layer % 2 == 0:
        # Front/back horizontal planks, like the colored face bands in the photo.
        for y in y_faces:
            add_box(0.0, y, z, beam_len, beam_w, course_z, color)
    else:
        # Perpendicular cross courses create the woven side columns and support
        # the next front/back layer at three contact points.
        for x in x_cols:
            add_box(x, 0.0, z, beam_w, beam_len * 0.72, course_z, color)

# Small raised top teeth, matching the upright green tabs at the top of the image.
top_color = COLORS[2]
top_z = course_z + layers * (2 * course_z) + 0.14
for x in x_cols:
    for y in y_faces:
        add_box(x, y, top_z, beam_w, beam_w, 0.25, top_color)

bodies_xml = "\n".join(domino_list)
xml = f"""{HEADER}  <worldbody>
    <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>
{bodies_xml}
  </worldbody>
</mujoco>
"""

with open("domino/basketweave.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Wrote basketweave.xml ({count} blocks)")
