import colorsys

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

# Basketweave tower parameters
# Long, thin blocks that span across the tower
block_thick = 0.06      # thin width (like thread)
block_depth = 0.30      # depth (Y dimension when horizontal)
block_height = 0.10     # vertical thickness per layer

grid_n = 5              # 5x5 crossing points
span = 2.0              # total span of crossing area
spacing = span / (grid_n - 1)  # distance between crossing points
half_span = span / 2.0

num_layers = 24         # 24 layers

# Colors: green, blue, pink/magenta, yellow
colors = [
    (0.2, 0.8, 0.2),   # green
    (0.2, 0.4, 0.9),   # blue  
    (0.9, 0.2, 0.6),   # pink/magenta
    (0.9, 0.8, 0.1),   # yellow
]

domino_list = []
count = 0

for layer in range(num_layers):
    color = colors[(layer // 2) % 4]
    z = block_height + layer * (2 * block_height)
    
    # Alternate direction by layer
    if layer % 2 == 0:
        # X-aligned blocks (along X axis)
        # Place one block per row, spanning full width
        for i in range(grid_n):
            y = -half_span + i * spacing
            # Block centered at origin, extends from -half_span to +half_span in X
            domino_list.append(f'    <body pos="0.0000 {y:.4f} {z:.4f}" euler="0 0 0">')
            domino_list.append(f'      <geom type="box" size="{half_span} {block_thick} {block_height}" rgba="{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            count += 1
    else:
        # Y-aligned blocks (along Y axis)
        for j in range(grid_n):
            x = -half_span + j * spacing
            domino_list.append(f'    <body pos="{x:.4f} 0.0000 {z:.4f}" euler="0 0 90">')
            domino_list.append(f'      <geom type="box" size="{half_span} {block_thick} {block_height}" rgba="{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} 1"/>')
            domino_list.append(f'      <freejoint/>')
            domino_list.append(f'    </body>')
            count += 1

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
