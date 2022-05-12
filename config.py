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
wall_break_chance = cc.get('wall_break_chance', 0.1)

# warning: making it True will worsen performance drastically
find_shortest_path = cc.get('find_shortest_path', False)

cursor_radius = cell_size * 0.85
ui_panel_height = 80
button_width = 120
button_height = 40
bottom_panel_margin = 35
min_window_width = button_width * 3 + 20

bg_color = arcade.color.BLACK
cell_color = arcade.color.WHITE
path_color = arcade.color.GREEN
cursor_color = path_color + (200,)
