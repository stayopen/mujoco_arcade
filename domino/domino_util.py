import numpy as np

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

DX = 1
DY = 3
DZ = 6
SCALE = 0.1
DXX = round(DX * SCALE, 4)
DYY = round(DY * SCALE, 4)
DZZ = round(DZ * SCALE, 4)


def write_path_xml(filename, px, py, pz=None, colors=None, tilt=15, min_dist=0.65):
    px = np.asarray(px)
    py = np.asarray(py)
    if pz is None:
        pz = np.full_like(px, DZZ)
    else:
        pz = np.asarray(pz)

    kept_x = [px[0]]
    kept_y = [py[0]]
    kept_z = [pz[0]]
    for i in range(1, len(px)):
        dx_i = px[i] - np.array(kept_x)
        dy_i = py[i] - np.array(kept_y)
        dz_i = pz[i] - np.array(kept_z)
        if np.min(np.hypot(np.hypot(dx_i, dy_i), dz_i)) >= min_dist:
            kept_x.append(px[i])
            kept_y.append(py[i])
            kept_z.append(pz[i])
        if len(kept_x) >= 300:
            break

    kx = np.array(kept_x)
    ky = np.array(kept_y)
    kz = np.array(kept_z)
    N = len(kept_x)
    angles = np.arctan2(np.gradient(ky), np.gradient(kx))

    if colors is None:
        import colorsys
        hues = np.linspace(0, 1, N, endpoint=False)
        colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]
    else:
        colors = colors[:N]

    domino_list = []
    for i in range(N):
        c = colors[i]
        euler_z = np.degrees(angles[i])
        tilt_y = tilt if i == 0 else 0
        domino_list.append(f'    <body pos="{kx[i]:.4f} {ky[i]:.4f} {kz[i]:.4f}" euler="0 {tilt_y:.1f} {euler_z:.1f}">')
        domino_list.append(f'      <geom type="box" size="{DXX:.4f} {DYY:.4f} {DZZ:.4f}" rgba="{c[0]:.3f} {c[1]:.3f} {c[2]:.3f} 1"/>')
        domino_list.append(f'      <freejoint/>')
        domino_list.append(f'    </body>')

    bodies_xml = "\n".join(domino_list)
    xml = f"""{HEADER}  <worldbody>
    <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>
    <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>
{bodies_xml}
  </worldbody>
</mujoco>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"Wrote {filename} ({N} blocks)")
