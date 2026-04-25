#!/bin/bash
uv run python domino/gen.py
uv run python domino/gen_linear.py
uv run python domino/gen_spiral.py
uv run python domino/gen_11tower.py
uv run python domino/gen_speedwall.py
