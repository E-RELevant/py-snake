"""
FILE: board_cell.py
DESCRIPTION: a 'BoardCell' class used for a 'snake' game.
"""
###############################################################################
#                                   Imports                                   #
###############################################################################
import game_utils
from typing import Tuple


###############################################################################
#                                  Constants                                  #
###############################################################################
MOVE_DELTA_MAPPING = {
    # (column, row)
    game_utils.UP: (0, 1),
    game_utils.DOWN: (0, -1),
    game_utils.RIGHT: (1, 0),
    game_utils.LEFT: (-1, 0)
}


###############################################################################
#                           Class & Inner Functions                           #
###############################################################################
class BoardCell:
    """
    A class representing a single board cell
    """

    def __init__(self, x_value: int, y_value: int, color: str) -> None:
        self.column = x_value
        self.row = y_value
        self.color = color

    # region get & set methods
    # region property: location
    def get_location(self) -> Tuple[int, int]:
        """
        Returns the location of the cell
        """
        return self.column, self.row

    def set_location(self, x_value: int, y_value: int) -> None:
        """
        Sets the location of the cell
        """
        self.column = x_value
        self.row = y_value

    # endregion property: location
    # region property: color
    def get_color(self) -> str:
        """
        Returns the color of the cell
        """
        return self.color

    def set_color(self, color: str) -> None:
        """
        Sets the color of the cell
        """
        self.color = color

    # endregion property: location
    # endregion get & set methods
    # region comparison methods
    def next_coord_in_direction(self, direction: str) -> Tuple[int, int]:
        """
        Locates the next coordinate in the current direction of the cell
        :param direction: the direction of the required coordinate
        :return: the next coordinate in the current direction of the cell
        """
        delta_col, delta_row = MOVE_DELTA_MAPPING.get(direction, (0, 0))
        return self.column + delta_col, self.row + delta_row
    # endregion comparison methods


if __name__ == "__main__":
    print("This script is part of the 'Snake' board game.\nYou should run:\n"
          "> python game_display.py [optional arguments|--help]")
