import math

import arcade

import config as cfg
from models import Maze


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

    def on_update(self, delta_time: float):
        self.update_maze()

    def update_maze(self):
        if self.is_generating:
            try:
                for _ in range(self.maze_iterations_per_frame):
                    old_x, old_y, x, y = next(self.maze_generator)
                    self.maze.remove_wall(old_x, old_y, x, y)
                    self.maze.grid[x][y] = True
            except StopIteration:
                self.is_generating = False
                self.is_maze_generated = True

    def generate_maze(self):
        if not self.is_generating:
            self.maze.reset_grid()
            self.is_generating = True
            self.maze_generator = self.maze.generate_with_dfs()
            self.path = None
            self.is_maze_generated = False

    def draw_maze(self):
        # todo improve
        for i, row in enumerate(self.maze.grid):
            for j, cell in enumerate(row):
                if cell:
                    arcade.draw_rectangle_filled(*self.maze.g_cells[i][j],
                                                 cfg.cell_size, cfg.cell_size, cfg.cell_color)

        for i, row in enumerate(self.maze.vwalls):
            for j, wall in enumerate(row):
                if wall:
                    arcade.draw_line(*self.maze.g_vwalls[i][j],
                                     cfg.cell_color, cfg.wall_width)

        for i, row in enumerate(self.maze.hwalls):
            for j, wall in enumerate(row):
                if wall:
                    arcade.draw_line(*self.maze.g_hwalls[i][j],
                                     cfg.cell_color, cfg.wall_width)

    def draw_path(self):
        if self.path is not None:
            arcade.draw_line_strip([self.maze.g_cells[x][y] for x, y in self.path],
                                   cfg.path_color, line_width=cfg.path_width)


def main():
    Game()
    arcade.run()


if __name__ == '__main__':
    main()
