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
DEFAULT_CHAIN_SPACING = 0.75
MAX_BLOCKS = 300


def _resample_chain(px, py, pz, spacing, max_blocks):
    points = np.column_stack([px, py, pz]).astype(float)
    finite = np.all(np.isfinite(points), axis=1)
    points = points[finite]
    if len(points) < 2:
        raise ValueError("A domino chain needs at least two finite points")

    seg = np.linalg.norm(np.diff(points, axis=0), axis=1)
    keep = np.concatenate([[True], seg > 1e-9])
    points = points[keep]
    if len(points) < 2:
        raise ValueError("A domino chain needs at least two distinct points")

    seg = np.linalg.norm(np.diff(points, axis=0), axis=1)
    distance = np.concatenate([[0.0], np.cumsum(seg)])
    total = distance[-1]
    sample_count = min(max_blocks, int(total / spacing) + 1)
    sample_at = np.arange(sample_count) * spacing

    chain = np.column_stack(
        [np.interp(sample_at, distance, points[:, axis]) for axis in range(3)]
    )
    return chain


def _resample_colors(colors, count):
    if colors is None:
        import colorsys
        hues = np.linspace(0, 1, count, endpoint=False)
        return [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

    colors = np.asarray(colors, dtype=float)
    if len(colors) == count:
        return colors
    if len(colors) == 1:
        return np.repeat(colors, count, axis=0)

    source_at = np.linspace(0, len(colors) - 1, count)
    lo = np.floor(source_at).astype(int)
    hi = np.ceil(source_at).astype(int)
    weight = (source_at - lo)[:, None]
    return colors[lo] * (1 - weight) + colors[hi] * weight


def write_path_xml(
    filename,
    px,
    py,
    pz=None,
    colors=None,
    tilt=28,
    min_dist=DEFAULT_CHAIN_SPACING,
    chain_spacing=None,
    max_blocks=MAX_BLOCKS,
):
    px = np.asarray(px)
    py = np.asarray(py)
    if pz is None:
        pz = np.full_like(px, DZZ, dtype=float)
    else:
        pz = np.asarray(pz)

    spacing = chain_spacing if chain_spacing is not None else min_dist
    chain = _resample_chain(px, py, pz, spacing, max_blocks)
    kx = chain[:, 0]
    ky = chain[:, 1]
    kz = chain[:, 2]
    N = len(chain)

    directions = np.diff(chain[:, :2], axis=0)
    directions = np.vstack([directions, directions[-1]])
    angles = np.arctan2(directions[:, 1], directions[:, 0])
    colors = _resample_colors(colors, N)

    domino_list = []
    for i in range(N):
        c = colors[i]
        euler_z = np.degrees(angles[i])
        tilt_y = tilt if i == 0 else 0
        center_z = kz[i]
        if i == 0 and tilt_y:
            theta = np.radians(abs(tilt_y))
            center_z += DZZ * np.cos(theta) + DXX * np.sin(theta) - DZZ
        name = "trigger" if i == 0 else f"domino_{i:03d}"
        domino_list.append(f'    <body name="{name}" pos="{kx[i]:.4f} {ky[i]:.4f} {center_z:.4f}" euler="0 {tilt_y:.1f} {euler_z:.1f}">')
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
    print(f"Wrote {filename} ({N} chain blocks, spacing={spacing:.2f})")
