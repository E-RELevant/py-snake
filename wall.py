"""
FILE: wall.py
DESCRIPTION: a 'Wall' class used for a 'snake' game.
"""
###############################################################################
#                                   Imports                                   #
###############################################################################
import game_utils
from typing import List, Set, Tuple
from board_cell import BoardCell


###############################################################################
#                           Class & Inner Functions                           #
###############################################################################
class Wall(BoardCell):
    """
    A class representing a 'wall' object, which is a list of three of
    BoardCell(s) colored blue
    """

    def __init__(self, center_cell_col_value: int, center_cell_row_value: int,
                 direction: str, color: str = "blue") -> None:
        super().__init__(center_cell_col_value, center_cell_row_value, color)
        self.direction: str = direction
        self.length: int = 3
        self.wall_cells: List[BoardCell] = self.create_wall_cells()

    # region get & set methods
    def get_wall_cells(self) -> List[BoardCell]:
        """
        Returns the list of all the wall cells
        """
        return self.wall_cells

    def get_wall_cells_locations(self) -> Set[Tuple[int, int]]:
        """
        Returns the list of all the wall cells locations
        """
        wall_cells_locations_set = set()
        for cell in self.wall_cells:
            wall_cells_locations_set.add(cell.get_location())
        return wall_cells_locations_set

    # endregion get & set methods
    # region action methods
    def create_wall_cells(self) -> List[BoardCell]:
        """
        Creates a list of 'wall' BoardCell(s)
        """
        if self.direction not in [game_utils.UP, game_utils.DOWN,
                                  game_utils.LEFT, game_utils.RIGHT]:
            return []

        wall_cells = []

        # add BoardCell(s) from negative length // 2 to length // 2
        for i in range(-(self.length // 2), self.length // 2 + 1):
            if self.direction in [game_utils.UP, game_utils.DOWN]:
                delta = (1 if self.direction == game_utils.UP else -1) * i
                cell_col_value = self.column
                cell_row_value = self.row + delta
            elif self.direction in [game_utils.LEFT, game_utils.RIGHT]:
                delta = (1 if self.direction == game_utils.RIGHT else -1) * i
                cell_col_value = self.column + delta
                cell_row_value = self.row
            new_cell = BoardCell(cell_col_value, cell_row_value, self.color)
            wall_cells.append(new_cell)

        return wall_cells

    def move(self) -> None:
        """
        Moves the wall one step in its direction
        """

        # get the new head coordinate
        new_head_col, new_head_row = \
            self.wall_cells[-1].next_coord_in_direction(self.direction)

        # pop the last tail cell
        self.wall_cells.pop(0)

        # create a new head
        new_cell = BoardCell(new_head_col, new_head_row, self.color)
        self.wall_cells.append(new_cell)

    # endregion action methods


if __name__ == "__main__":
    print("This script is part of the 'Snake' board game.\nYou should run:\n"
          "> python game_display.py [optional arguments|--help]")
