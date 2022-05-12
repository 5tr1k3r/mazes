import random
from typing import List, Tuple, Optional, Set

import config as cfg

Coords = Tuple[float, float]
LineCoords = Tuple[float, float, float, float]
Node = Tuple[int, int]
FullPath = List[Node]


class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = None
        self.vwalls = None
        self.hwalls = None
        self.bottom_left_y = cfg.ui_panel_height
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
        curr_y = self.bottom_left_y + cfg.wall_width + cfg.cell_size / 2
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
        h = (cfg.cell_size + cfg.wall_width) * self.height + cfg.wall_width + self.bottom_left_y

        return w, h

    def get_wall_coords(self, start_x, start_y,
                        offset_x, offset_y, is_vertical: bool) -> List[List[LineCoords]]:
        coords = []
        height = self.height
        width = self.width
        if is_vertical:
            width -= 1
        else:
            height -= 1

        curr_y = start_y
        for j in range(height):
            coords.append([])
            curr_x = start_x

            for i in range(width):
                coords[j].append((curr_x, curr_y, curr_x + offset_x, curr_y + offset_y))
                curr_x += cfg.cell_size + cfg.wall_width

            curr_y += cfg.cell_size + cfg.wall_width

        return coords

    def get_vertical_wall_coords(self) -> List[List[LineCoords]]:
        return self.get_wall_coords(start_x=cfg.wall_width * 1.5 + cfg.cell_size,
                                    start_y=self.bottom_left_y + cfg.wall_width,
                                    offset_x=0,
                                    offset_y=cfg.cell_size,
                                    is_vertical=True)

    def get_horizontal_wall_coords(self) -> List[List[LineCoords]]:
        return self.get_wall_coords(start_x=cfg.wall_width,
                                    start_y=self.bottom_left_y + cfg.wall_width * 1.5 + cfg.cell_size,
                                    offset_x=cfg.cell_size,
                                    offset_y=0,
                                    is_vertical=False)

    def find_path_from_x_to_y(self,
                              start: Optional[Node] = None,
                              end: Optional[Node] = None) -> FullPath:
        if start is None:
            start = (0, 0)

        if end is None:
            end = (self.height - 1, self.width - 1)

        # currently there will only be one path that is produced
        # but decided to kinda future-proof it
        # and look for the shortest path anyway
        shortest_path = []
        shortest_path_length = float('inf')
        for path in self.dfs_paths(start, end):
            if len(path) < shortest_path_length:
                shortest_path_length = len(path)
                shortest_path = path

        return shortest_path

    def dfs_paths(self, start: Node, end: Node):
        queue = [(start, [start])]
        seen = set()
        while queue:
            cell, path = queue.pop()
            if cell in seen:
                continue

            if path[-1] == end:
                yield path

            seen.add(cell)
            for candidate in self.get_candidates(cell, path):
                queue.append((candidate, path + [candidate]))

    def get_neighbors(self, node: Node) -> Set[Node]:
        x, y = node
        all_neighbors = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]

        return {(x, y) for x, y in all_neighbors if 0 <= x < self.height and 0 <= y < self.width}

    def get_candidates(self, start: Node, path: FullPath) -> Set[Node]:
        candidates = self.get_neighbors(start) - set(path)
        return self.wall_filter(start, candidates)

    def wall_filter(self, start: Node, candidates: Set[Node]) -> Set[Node]:
        result = set()
        old_x, old_y = start
        for c in candidates:
            x, y = c

            # horizontal movement
            if old_x == x:
                miny = min(old_y, y)
                if self.vwalls[x][miny]:
                    result.add(c)

            # vertical movement
            else:
                minx = min(old_x, x)
                if self.hwalls[minx][y]:
                    result.add(c)

        return result
