"""
FILE: snake.py
DESCRIPTION: a 'Snake' class used for a 'snake' game.
"""
###############################################################################
#                                   Imports                                   #
###############################################################################
import game_utils
from typing import Optional, List, Set, Tuple
from board_cell import BoardCell, MOVE_DELTA_MAPPING


###############################################################################
#                           Class & Inner Functions                           #
###############################################################################
class Snake(BoardCell):
    """
    A class representing a 'snake' object, which is a list of BoardCells
    colored black
    """

    def __init__(self, head_col, head_row, length=3, color="black") -> None:
        super().__init__(head_col, head_row, color)
        self.head_col: int
        self.head_row: int
        self.color: str

        self.init_length = length
        self.direction = game_utils.UP
        self.cells_to_be_added = 0

        # [BoardCell(='TAIL'), BoardCell, ..., BoardCell(='HEAD')]
        self.__snake_cells = []
        self.__snake_cells_locations = set()

        # init snake cells
        for i in range(self.init_length):
            new_cell = BoardCell(head_col, head_row - i, color)
            self.__snake_cells.append(new_cell)
            self.__snake_cells_locations.add((head_col, head_row - i))
        self.__snake_cells.reverse()

    # region get & set methods
    def get_length(self) -> int:
        """
        Returns the snake's length
        """
        return len(self.__snake_cells)

    def get_snake_cells(self) -> List[BoardCell]:
        """
        Returns the snake's cells
        """
        return self.__snake_cells

    def get_snake_cells_locations(self) -> Set[Tuple[int, int]]:
        """
        Returns the snake's cells' locations
        """
        return self.__snake_cells_locations

    # endregion get & set methods
    # region action methods
    def update_direction(self, key_clicked) -> None:
        """
        Changes the direction of the snake
        :param key_clicked: the key clicked by the user
        :return: None
        """
        if key_clicked is None:
            return None

        # get the required (='new') coord
        head_col, head_row = self.__snake_cells[-1].get_location()
        delta_col, delta_row = MOVE_DELTA_MAPPING.get(key_clicked, (0, 0))
        new_head_coord = head_col + delta_col, head_row + delta_row

        # conditions to verify
        # - 1: key clicked is not the same as the current defined
        is_key_clicked_not_current_direction = key_clicked != self.direction
        # - 2: key clicked is allowed
        if len(self.__snake_cells) == 1:
            is_key_clicked_allowed = True
        else:
            first_tail_cell_coord = self.__snake_cells[-2].get_location()
            is_key_clicked_allowed = new_head_coord != first_tail_cell_coord

        # update direction if conditions are met
        if is_key_clicked_allowed and is_key_clicked_not_current_direction:
            self.direction = key_clicked

    def move(self) -> None:
        """
        Moves the snake one step in its direction
        """
        # get the new head coordinate
        new_head_col, new_head_row = \
            self.__snake_cells[-1].next_coord_in_direction(self.direction)

        # pop the last tail cell (if did not eat an apple)
        if self.cells_to_be_added > 0:
            self.cells_to_be_added -= 1
        else:
            tail_cell = self.__snake_cells.pop(0)
            self.__snake_cells_locations.remove(tail_cell.get_location())

        # create a new head
        new_cell = BoardCell(new_head_col, new_head_row, self.color)
        self.__snake_cells.append(new_cell)
        self.__snake_cells_locations.add(new_cell.get_location())

    def cut_tail(self, coordinate: Tuple[int, int]) -> None:
        """
        Removes the tail of the snake
        :param coordinate: the coordinate of the tail to cut up to
        :return: None
        """
        try:
            index, cell = self.__get_cell_by_location(coordinate)

            self.__snake_cells = self.__snake_cells[index + 1:]
            self.__regenerage_snake_cell_locations()
        except ValueError:
            # something real scatchy just happened
            return

    def __get_cell_by_location(self, coordinate: Tuple[int, int]) -> \
            Tuple[int, BoardCell]:
        """
        Returns the cell at the given coordinate
        :param coordinate: the coordinate of the cell to get
        :return: the cell at the given coordinate
        """
        for index, cell in enumerate(self.__snake_cells):

            if cell.get_location() == coordinate:
                return index, cell

        # something real scatchy just happene
        raise ValueError

    def grow(self) -> None:
        """
        Adds three to 'cells_to_be_added'
        :return: None
        """
        self.cells_to_be_added += 3

    def __regenerage_snake_cell_locations(self) -> None:
        """
        Regenerates the snake's cell locations (due to a major change)
        :return: None
        """
        new_snake_cell_locations: Set[Tuple[int, int]] = set()
        for cell in self.__snake_cells:
            new_snake_cell_locations.add(cell.get_location())

        self.__snake_cells_locations = new_snake_cell_locations

    # endregion action methods
    # region comparion methods
    def compare_to_head(self, coordinate: Tuple[int, int]) -> bool:
        """
        Checks if a given coordinate is in the same location as the head of
        the snake
        :param coordinate: a coordinate of a BoardCell
        :return: True if the coordinate is in the same location as the head,
                 False otherwise
        """
        snake_head_location = self.__snake_cells[-1].get_location()
        return True if coordinate == snake_head_location else False

    def is_collided(self, game_object: List[BoardCell]) -> \
            Tuple[bool, Optional[Tuple[int, int]]]:
        """
        Checks if the snake is collided with another game object
        :param game_object: the game object to compare to
        :return: True if the snake is collided with the game object,
                 False otherwise
        """
        for cell in game_object:
            if cell.get_location() in self.__snake_cells_locations:
                return True, cell.get_location()

        return False, None

    def is_tangled(self) -> bool:
        """
        Checks whether the snake is tangled (ate itself)
        :return: True if the snake not tangled, False otherwise
        """
        not_tangled = len(self.__snake_cells) > len(
            self.__snake_cells_locations)
        return False if not_tangled else True
    # endregion comparion methods


if __name__ == "__main__":
    print("You should run:\n"
          "> python game_display.py [optional arguments|--help]")
