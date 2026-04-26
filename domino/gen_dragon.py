import numpy as np
import colorsys
from domino_util import write_path_xml

# Open dragon-like path.  A true dragon curve self-touches, which makes
# physical domino blocks overlap; this keeps the winding silhouette chainable.
t = np.linspace(0, 1, 200000)
px = 14.0 * (t - 0.5)
py = 2.4 * np.sin(3.0 * np.pi * t) + 0.8 * np.sin(17.0 * np.pi * t)

hues = np.linspace(0, 1, len(px), endpoint=False)
colors = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hues]

write_path_xml("domino/dragon.xml", px, py, colors=colors, chain_spacing=0.75)
