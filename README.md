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
