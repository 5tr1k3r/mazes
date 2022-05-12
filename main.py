import math

import arcade

import config as cfg
from models import Maze

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
        self.path = None
        self.maze_iterations_per_frame = math.ceil(cfg.maze_width * cfg.maze_height / (60 * cfg.max_generation_time))
        self.maze_shape_list = arcade.ShapeElementList()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
        elif symbol == arcade.key.SPACE:
            self.generate_maze()
        elif symbol == arcade.key.ENTER:
            if self.is_maze_generated:
                self.path = self.maze.find_path()

    def on_draw(self):
        self.clear()

        self.draw_maze()
        self.draw_path()
        self.show_fps()

    def on_update(self, delta_time: float):
        self.update_maze()

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
            self.maze_shape_list = arcade.ShapeElementList()
            self.maze.reset_grid()
            self.is_generating = True
            self.maze_generator = self.maze.generate_with_dfs()
            self.path = None
            self.is_maze_generated = False

    def draw_maze(self):
        self.maze_shape_list.draw()

    def draw_path(self):
        if self.path is not None:
            arcade.draw_line_strip([self.maze.g_cells[x][y] for x, y in self.path],
                                   cfg.path_color, line_width=cfg.path_width)

    @staticmethod
    def show_fps():
        # Get FPS for the last 60 frames
        text = f"FPS: {arcade.get_fps(60):5.1f}"
        arcade.draw_text(text, 10, 10, arcade.color.SMOKY_BLACK, 22)


def main():
    Game()
    arcade.run()


if __name__ == '__main__':
    main()
