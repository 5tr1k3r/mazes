import math
from typing import Tuple, Optional

import arcade

import config as cfg
from models import Maze, Node

arcade.enable_timings()


class Game(arcade.Window):
    def __init__(self):
        self.maze = Maze(cfg.maze_width, cfg.maze_height)
        width, height = self.maze.get_window_dimensions()
        super().__init__(width, height, 'Mazes', center_window=True)
        self.is_generating = False
        self.is_maze_generated = False
        arcade.set_background_color(cfg.bg_color)
        self.maze_generator = None
        self.maze_iterations_per_frame = math.ceil(cfg.maze_width * cfg.maze_height / (60 * cfg.max_generation_time))
        self.maze_shape_list = arcade.ShapeElementList()
        self.path_shape_list = arcade.ShapeElementList()
        self.is_selecting_start = False
        self.is_selecting_exit = False
        self.custom_start = None

    def on_key_press(self, symbol: int, modifiers: int):
        if self.is_selecting_cell():
            if symbol in (arcade.key.ESCAPE, arcade.key.E):
                self.stop_selecting_cell()

            return

        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
        elif symbol == arcade.key.SPACE:
            self.generate_maze()
        elif symbol == arcade.key.ENTER:
            self.find_default_path()
        elif symbol == arcade.key.E:
            self.find_custom_path()

    def on_draw(self):
        self.clear()

        self.draw_maze()
        self.draw_path()
        self.draw_start_marker()
        self.draw_select_cell_text()
        self.show_fps()

    def on_update(self, delta_time: float):
        self.update_maze()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.is_selecting_cell():
            lane_x, lane_y = self.select_cell(x, y)

            if self.is_selecting_start:
                self.custom_start = lane_x, lane_y
                self.is_selecting_start = False
                self.is_selecting_exit = True
            else:
                if (lane_x, lane_y) == self.custom_start:
                    print('start and exit should be different')
                    return

                self.find_path(self.custom_start, (lane_x, lane_y))
                self.stop_selecting_cell()

    def reset(self):
        self.is_generating = False
        self.is_maze_generated = False
        self.maze_shape_list = arcade.ShapeElementList()
        self.path_shape_list = arcade.ShapeElementList()
        self.is_selecting_start = False
        self.is_selecting_exit = False
        self.custom_start = None

    def update_maze(self):
        if self.is_generating:
            if cfg.visualize_generation:
                try:
                    for _ in range(self.maze_iterations_per_frame):
                        old_x, old_y, x, y = next(self.maze_generator)
                        self.update_cell(old_x, old_y, x, y)

                except StopIteration:
                    self.is_generating = False
                    self.is_maze_generated = True
            else:
                for old_x, old_y, x, y in self.maze_generator:
                    self.update_cell(old_x, old_y, x, y)

                self.is_generating = False
                self.is_maze_generated = True

    def update_cell(self, old_x: int, old_y: int, x: int, y: int):
        self.maze.grid[x][y] = True
        rect = arcade.create_rectangle_filled(*self.maze.g_cells[x][y],
                                              cfg.cell_size, cfg.cell_size, cfg.cell_color)
        self.maze_shape_list.append(rect)

        if old_x == x and old_y == y:
            return

        # vertical wall
        if old_x == x:
            miny = min(old_y, y)
            self.maze.vwalls[x][miny] = True
            line = arcade.create_line(*self.maze.g_vwalls[x][miny],
                                      cfg.cell_color, cfg.wall_width)

        # horizontal wall
        else:
            minx = min(old_x, x)
            self.maze.hwalls[minx][y] = True
            line = arcade.create_line(*self.maze.g_hwalls[minx][y],
                                      cfg.cell_color, cfg.wall_width)

        self.maze_shape_list.append(line)

    def generate_maze(self):
        if not self.is_generating:
            self.reset()
            self.maze.reset_grid()
            self.is_generating = True
            self.maze_generator = self.maze.generate_with_dfs()

    def draw_maze(self):
        self.maze_shape_list.draw()

    def draw_path(self):
        self.path_shape_list.draw()

    @staticmethod
    def show_fps():
        # Get FPS for the last 60 frames
        text = f"FPS: {arcade.get_fps(60):5.1f}"
        arcade.draw_text(text, 10, 10, arcade.color.WHITE, 12)

    def draw_select_cell_text(self):
        if not self.is_selecting_cell():
            return

        if self.is_selecting_start:
            target = 'start'
        else:
            target = 'exit'

        arcade.draw_text(f'Selecting {target}', self.width / 2, 10, arcade.color.WHITE, 16,
                         anchor_x='center', anchor_y='baseline')

    def draw_start_marker(self):
        if self.is_selecting_exit and self.custom_start is not None:
            x, y = self.custom_start
            arcade.draw_circle_filled(*self.maze.g_cells[x][y],
                                      cfg.cell_size * 0.85, cfg.path_color + (200,))

    def find_path(self,
                  start: Optional[Node] = None,
                  end: Optional[Node] = None):
        self.path_shape_list = arcade.ShapeElementList()
        path = self.maze.find_path_from_x_to_y(start, end)
        lines = arcade.create_line_strip([self.maze.g_cells[x][y] for x, y in path],
                                         cfg.path_color, line_width=cfg.path_width)
        self.path_shape_list.append(lines)

    def find_default_path(self):
        if self.is_maze_generated:
            self.find_path()

    def find_custom_path(self):
        if self.is_maze_generated:
            self.is_selecting_start = True

    def is_selecting_cell(self) -> bool:
        return self.is_selecting_start or self.is_selecting_exit

    def stop_selecting_cell(self):
        self.is_selecting_start = False
        self.is_selecting_exit = False
        self.custom_start = None

    def select_cell(self, mouse_x: float, mouse_y: float) -> Tuple[int, int]:
        low_dist = float('inf')
        low_x = 0
        low_y = 0

        for i, row in enumerate(self.maze.g_cells):
            for j, (x, y) in enumerate(row):
                dist = math.hypot(mouse_x - x, mouse_y - y)
                if dist < low_dist:
                    low_dist = dist
                    low_x = i
                    low_y = j

        return low_x, low_y


def main():
    Game()
    arcade.run()


if __name__ == '__main__':
    main()
