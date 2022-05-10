import random
from typing import List, Tuple
import config as cfg

Coords = Tuple[float, float]
LineCoords = Tuple[float, float, float, float]


class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = None
        self.vwalls = None
        self.hwalls = None
        self.g_cells = self.get_cell_coords()
        self.g_vwalls = self.get_vertical_wall_coords()
        self.g_hwalls = self.get_horizontal_wall_coords()

        self.reset_grid()

    def reset_grid(self):
        self.grid = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.vwalls = [[False for _ in range(self.width - 1)] for _ in range(self.height)]
        self.hwalls = [[False for _ in range(self.width)] for _ in range(self.height - 1)]

    def get_cell_coords(self) -> List[List[Coords]]:
        coords = []
        curr_y = cfg.wall_width + cfg.cell_size / 2
        for j in range(self.height):
            coords.append([])
            curr_x = cfg.wall_width + cfg.cell_size / 2

            for i in range(self.width):
                coords[j].append((curr_x, curr_y))
                curr_x += cfg.cell_size + cfg.wall_width

            curr_y += cfg.cell_size + cfg.wall_width

        return coords

    def generate_with_dfs(self):
        queue = [(0, 0, 0, 0)]
        seen = set()
        while queue:
            old_x, old_y, x, y = queue.pop()
            if (x, y) in seen:
                continue

            seen.add((x, y))
            yield old_x, old_y, x, y

            temp_queue = []

            for dx in (-1, 1):
                nx = x + dx
                if 0 <= nx < self.height and not self.grid[nx][y]:
                    temp_queue.append((x, y, nx, y))

            for dy in (-1, 1):
                ny = y + dy
                if 0 <= ny < self.width and not self.grid[x][ny]:
                    temp_queue.append((x, y, x, ny))

            random.shuffle(temp_queue)
            queue += temp_queue

    def get_window_dimensions(self) -> Tuple[int, int]:
        w = (cfg.cell_size + cfg.wall_width) * self.width + cfg.wall_width
        h = (cfg.cell_size + cfg.wall_width) * self.height + cfg.wall_width

        return w, h

    def remove_wall(self, old_x: int, old_y: int, x: int, y: int):
        if old_x == x and old_y == y:
            return

        # vertical wall
        if old_x == x:
            miny = min(old_y, y)
            self.vwalls[x][miny] = True

        # horizontal wall
        elif old_y == y:
            minx = min(old_x, x)
            self.hwalls[minx][y] = True

    def get_vertical_wall_coords(self) -> List[List[LineCoords]]:
        coords = []
        curr_y = cfg.wall_width
        for j in range(self.height):
            coords.append([])
            curr_x = cfg.wall_width * 1.5 + cfg.cell_size

            for i in range(self.width - 1):
                coords[j].append((curr_x, curr_y, curr_x, curr_y + cfg.cell_size))
                curr_x += cfg.cell_size + cfg.wall_width

            curr_y += cfg.cell_size + cfg.wall_width

        return coords

    def get_horizontal_wall_coords(self) -> List[List[LineCoords]]:
        coords = []
        curr_y = cfg.wall_width * 1.5 + cfg.cell_size
        for j in range(self.height - 1):
            coords.append([])
            curr_x = cfg.wall_width

            for i in range(self.width):
                coords[j].append((curr_x, curr_y, curr_x + cfg.cell_size, curr_y))
                curr_x += cfg.cell_size + cfg.wall_width

            curr_y += cfg.cell_size + cfg.wall_width

        return coords
