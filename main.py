import arcade

import config as cfg
from models import Maze


class Game(arcade.Window):
    def __init__(self):
        self.maze = Maze(cfg.maze_width, cfg.maze_height)
        width, height = self.maze.get_window_dimensions()
        super().__init__(width, height, 'Mazes', center_window=True)
        self.is_generating = False
        arcade.set_background_color(cfg.bg_color)
        self.maze_generator = None

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
        elif symbol == arcade.key.SPACE:
            self.generate_maze()

    def on_draw(self):
        self.clear()
        self.draw_maze()

    def on_update(self, delta_time: float):
        if self.is_generating:
            try:
                old_x, old_y, x, y = next(self.maze_generator)
                self.maze.remove_wall(old_x, old_y, x, y)
                self.maze.grid[x][y] = True
            except StopIteration:
                self.is_generating = False

    def generate_maze(self):
        if not self.is_generating:
            self.maze.reset_grid()
            self.is_generating = True
            self.maze_generator = self.maze.generate_with_dfs()

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


def main():
    Game()
    arcade.run()


if __name__ == '__main__':
    main()
