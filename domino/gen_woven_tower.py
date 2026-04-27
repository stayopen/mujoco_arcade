HEADER = """<mujoco>
  <visual>
    <headlight diffuse="0.7 0.7 0.7" ambient="0.15 0.15 0.15" specular="0 0 0"/>
    <rgba haze="0.12 0.18 0.25 1"/>
    <global azimuth="132" elevation="-16"/>
  </visual>
  <asset>
    <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0 0 0" width="512" height="3072"/>
    <texture type="2d" name="groundplane" builtin="checker" mark="edge" rgb1="0.2 0.3 0.4" rgb2="0.1 0.2 0.3" markrgb="0.8 0.8 0.8" width="300" height="300"/>
    <material name="groundplane" texture="groundplane" texuniform="true" texrepeat="5 5" reflectance="0.2"/>
  </asset>
"""

# Bright toy-block colors matching the reference tower.
COLORS = [
    (0.94, 0.05, 0.42),  # magenta
    (0.03, 0.33, 0.88),  # blue
    (0.00, 0.55, 0.18),  # green
    (0.96, 0.77, 0.02),  # yellow
]

# The tower is built as a stable log-cabin weave.  One course has split
# front/back planks; the next course has depth planks that support those splits.
course_h = 0.11
beam_w = 0.13
depth_half = 0.74
x_cols = [-1.02, -0.34, 0.34, 1.02]
y_faces = [-0.62, 0.62]
layers = 30

domino_list = []
count = 0


def add_box(x, y, z, sx, sy, sz, rgba):
    global count
    domino_list.append(f'    <body pos="{x:.4f} {y:.4f} {z:.4f}" euler="0 0 0">')
    domino_list.append(
        f'      <geom type="box" size="{sx:.4f} {sy:.4f} {sz:.4f}" '
        f'rgba="{rgba[0]:.3f} {rgba[1]:.3f} {rgba[2]:.3f} 1"/>'
    )
    domino_list.append('      <freejoint/>')
    domino_list.append('    </body>')
    count += 1


for layer in range(layers):
    rgba = COLORS[layer % len(COLORS)]
    z = course_h + layer * (2 * course_h)

    if layer % 2 == 0:
        # Three front/back planks per face.  The seams become the vertical
        # window strips visible in the reference image.
        for y in y_faces:
            for left, right in zip(x_cols[:-1], x_cols[1:]):
                span_half = (right - left) / 2 + 0.03
                add_box((left + right) / 2, y, z, span_half, beam_w, course_h, rgba)
    else:
        # Four perpendicular planks.  Their ends show up as stacked colored
        # blocks on the front face and support the next split-plank course.
        for x in x_cols:
            add_box(x, 0.0, z, beam_w, depth_half, course_h, rgba)

# Upright green tabs on top, matching the raised prongs in the photo.
top_color = COLORS[2]
top_base = layers * (2 * course_h)
for x in x_cols:
    for y in y_faces:
        add_box(x, y, top_base + 0.24, beam_w, beam_w, 0.24, top_color)

bodies_xml = "\n".join(domino_list)
xml = f"""{HEADER}  <worldbody>
    <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>
{bodies_xml}
  </worldbody>
</mujoco>
"""

with open("domino/woven_tower.xml", "w", encoding="utf-8") as f:
    f.write(xml)

print(f"Wrote woven_tower.xml ({count} blocks)")
