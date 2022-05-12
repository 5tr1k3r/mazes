Requirements
------------
- Python 3.9
- [arcade](https://pypi.org/project/arcade/)
- [toml](https://pypi.org/project/toml/)

Hotkeys
-------
- `Space` - generate a maze
- `Enter` - find a path from the bottom left to the top right corner
- `E` - select a custom path with the mouse and find the solution
- `B` - break the remaining walls with 10% chance per wall (configurable).
Warning: in most cases makes pathfinding *significantly* slower,
especially if you're looking for the shortest path.
- `Esc` - quit or exit path selection mode

Custom Config
--------------
You can create `custom_config.toml` file in the root folder and override some settings without having to edit `config.py`.
For example:
```
maze_width = 10
maze_height = 15

cell_size = 20
wall_width = 10
```