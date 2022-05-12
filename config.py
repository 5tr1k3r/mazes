import arcade
import toml

try:
    with open('custom_config.toml') as f:
        cc = toml.load(f)
except FileNotFoundError:
    cc = {}

maze_width = cc.get('maze_width', 20)
maze_height = cc.get('maze_height', 20)

cell_size = cc.get('cell_size', 25)
wall_width = cc.get('wall_width', 5)
path_width = cc.get('path_width', 8)
max_generation_time = cc.get('max_generation_time', 5.0)
visualize_generation = cc.get('visualize_generation', True)
fps_is_shown = cc.get('fps_is_shown', False)

ui_panel_height = 80
button_width = 120
button_height = 40
bottom_panel_margin = 35

bg_color = arcade.color.BLACK
cell_color = arcade.color.WHITE
path_color = arcade.color.GREEN
