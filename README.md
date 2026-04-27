# use start

# first run
uv sync

# visualize an xml
uv run python -m mujoco.viewer -mjcf=mesh3d/test_mesh.xml

uv run python -m mujoco.viewer -mjcf=mesh3d/domino.xml

# generate and visualize domino scenes
bash domino/gen_all.sh

uv run python -m mujoco.viewer -mjcf=domino/domino_tower.xml
uv run python -m mujoco.viewer -mjcf=domino/domino1.xml
uv run python -m mujoco.viewer -mjcf=domino/domino2.xml
uv run python -m mujoco.viewer -mjcf=domino/domino1x1tower.xml
uv run python -m mujoco.viewer -mjcf=domino/speedwall.xml
uv run python -m mujoco.viewer -mjcf=domino/pyramid.xml
uv run python -m mujoco.viewer -mjcf=domino/doublehelix.xml
uv run python -m mujoco.viewer -mjcf=domino/castle.xml
uv run python -m mujoco.viewer -mjcf=domino/zigzag_tower.xml
uv run python -m mujoco.viewer -mjcf=domino/spiral_tower.xml
uv run python -m mujoco.viewer -mjcf=domino/colosseum.xml
uv run python -m mujoco.viewer -mjcf=domino/basketweave.xml
uv run python -m mujoco.viewer -mjcf=domino/cascade.xml
uv run python -m mujoco.viewer -mjcf=domino/fanwall.xml
uv run python -m mujoco.viewer -mjcf=domino/zigzagwall.xml
uv run python -m mujoco.viewer -mjcf=domino/spiralwall.xml
uv run python -m mujoco.viewer -mjcf=domino/dualpeaks.xml
uv run python -m mujoco.viewer -mjcf=domino/heart.xml
uv run python -m mujoco.viewer -mjcf=domino/star.xml
uv run python -m mujoco.viewer -mjcf=domino/lissajous.xml
uv run python -m mujoco.viewer -mjcf=domino/stairs.xml
uv run python -m mujoco.viewer -mjcf=domino/maze.xml
uv run python -m mujoco.viewer -mjcf=domino/bounce.xml
uv run python -m mujoco.viewer -mjcf=domino/flower.xml
uv run python -m mujoco.viewer -mjcf=domino/tree.xml
uv run python -m mujoco.viewer -mjcf=domino/snake.xml
uv run python -m mujoco.viewer -mjcf=domino/gear.xml
uv run python -m mujoco.viewer -mjcf=domino/wavegrid.xml
uv run python -m mujoco.viewer -mjcf=domino/arch.xml
uv run python -m mujoco.viewer -mjcf=domino/blackhole.xml
uv run python -m mujoco.viewer -mjcf=domino/mandala.xml
uv run python -m mujoco.viewer -mjcf=domino/rollercoaster.xml
uv run python -m mujoco.viewer -mjcf=domino/city.xml
uv run python -m mujoco.viewer -mjcf=domino/dragon.xml
