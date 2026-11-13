# Pygame Platform Game

## Prerequisites

- Clone / fork this repo in the ADLC-Day-Of-Learning organization. Give it a unique name when you fork the repository. For example, prefix the repository with your username: `dmacpher-plaform-game`.
- Download the Fullsend CLI on your laptop and install agents on your cloned repository
- Install `uv` on your laptop, then set up and run the game with it:
  ```bash
  uv python install 3.13   # pygame has prebuilt wheels for 3.13, not 3.14+
  uv sync
  ```
  This creates a virtualenv with Python 3.13 (pinned in `.python-version`) and installs pygame into it.

## How the game works

The game is a single-file pygame platformer (`platformer.py`). Run it with:

```bash
uv run platformer.py
```

- **Move:** arrow keys or `A`/`D`
- **Jump:** `SPACE`, `W`, or `Up` (release early for a shorter hop)
- **Goal:** collect all 6 coins, then touch the red flag to win
- **R** restarts the game at any time. Falling off the bottom of the screen respawns you at the start

The player has gravity, variable jump height, and per-axis collision resolution against the platforms. Reaching the flag after collecting every coin shows the win screen.
