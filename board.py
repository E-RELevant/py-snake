"""
FILE: board.py
DESCRIPTION: a 'Board' class used for a 'snake' game.
"""
###############################################################################
#                                   Imports                                   #
###############################################################################
import game_utils
from typing import Optional, List, Tuple
from board_cell import BoardCell
from snake import Snake
from wall import Wall
from game_display import GameDisplay


###############################################################################
#                           Class & Inner Functions                           #
###############################################################################
class Board:
    """
    A 'SnakeGame' class used for a 'snake' game
    """

    def __init__(self, is_debug: bool = False) -> None:
        self.width: int = game_utils.size.width
        self.height: int = game_utils.size.height
        self.__key_clicked: Optional[str] = None
        self.__walls: List[Wall] = []
        self.__apples: List[BoardCell] = []
        self.__rounds: int = 0
        self.__score: int = 0
        self.is_debug: bool = is_debug
        self.is_over: bool = False
        self.snake = Snake(self.width // 2, self.height // 2, length=3)

    # region get & set methods
    # region property: rounds
    def get_rounds(self) -> int:
        """
        Returns the board's current round
        """
        return self.__rounds

    def add_round(self) -> None:
        """
        Adds to the total rounds
        """
        self.__rounds += 1

    # endregion property: rounds
    # region property: score
    def get_score(self) -> int:
        """
        Returns the board's current score
        """
        return self.__score

    def increase_score(self, value: int) -> None:
        """
        Adds to the total score
        """
        self.__score += value

    # endregion property: score
    # endregion get & set methods
    # region action methods
    def read_key(self, key_clicked: Optional[str]) -> None:
        """
        Reads the key pressed by the user
        :param key_clicked: the key pressed by the user
        :return: None
        """
        self.__key_clicked = key_clicked

    def update_moving_objects(self) -> None:
        """
        Updates all moving objects in the game
        """
        # region update walls
        if self.__rounds % 2 == 0:
            for wall in self.__walls:
                wall.move()
        self.remove_walls()
        # endregion update walls
        # region update snake
        if not self.is_debug:
            self.snake.update_direction(self.__key_clicked)
            self.snake.move()
        # endregion update snake

    def draw_list_of_board_cells(self, list_of_board_cells: List[BoardCell],
                                 gd: GameDisplay) -> None:
        """
        Draws all BoardCell(s) from a given list
        :param list_of_board_cells: a list of BoardCell(s)
        :param gd: a GameDisplay
        :return: None
        """
        for cell in list_of_board_cells:
            cell_row, cell_col = cell.get_location()

            # verify in board boundaries
            if self.is_coord_in_board_boundaries((cell_row, cell_col)):
                cell_color = cell.get_color()
                gd.draw_cell(cell_row, cell_col, cell_color)

    def draw_board(self, gd: GameDisplay) -> None:
        """
        Draws the board
        :param gd: a GameDisplay
        :return: None
        """
        # draws apples before walls, so if a wall ran into an apple,
        # the wall will be drawn on top of it

        # apples
        self.draw_list_of_board_cells(self.__apples, gd)

        # snake
        if not self.is_debug:
            self.draw_list_of_board_cells(self.snake.get_snake_cells(), gd)

        # walls
        for wall in self.__walls:
            self.draw_list_of_board_cells(wall.get_wall_cells(), gd)

    # endregion action methods
    # region comparion methods
    def is_coord_in_board_boundaries(self, coordinate: Tuple[int, int]) -> \
            bool:
        """
        Checks whther the given coordinate is in the board boundaries
        :param coordinate: a coordinate of a board cell
        :return: True if the coordinate is in the board boundaries else False
        """
        if not (0 <= coordinate[0] < self.width):
            return False
        if not (0 <= coordinate[1] < self.height):
            return False
        return True

    # endregion comparion methods
    # region game objects methods
    # region walls
    def get_walls(self) -> List[Wall]:
        """
        Returns a list of all the walls on the board
        """
        return self.__walls

    def is_wall_valid_to_place(self, wall: Wall) -> bool:
        """
        Checks whether all the wall's cells are currently empty on the
        board, therefore it is valid to place
        :param wall: a new wall candidate
        :return: True if all cells are empty, False otherwise
        """
        for cell in wall.wall_cells:
            # snake position comparions
            if not self.is_debug:
                if cell.get_location() in \
                        self.snake.get_snake_cells_locations():
                    return False

            # existing walls comparions
            for existing_wall in self.__walls:
                if cell.get_location() in \
                        existing_wall.get_wall_cells_locations():
                    return False

            # existing apples comparions
            for existing_apple in self.__apples:
                if cell.get_location() == existing_apple.get_location():
                    return False

        return True

    def add_wall(self) -> bool:
        """
        Adds a wall to the board
        :return: True if the wall was added, False otherwise
        """
        new_wall_col, new_wall_row, new_wall_direction = \
            game_utils.get_random_wall_data()

        # verify conditions
        # - 1: in board's boundaries
        wall_in_boundaries = \
            self.is_coord_in_board_boundaries((new_wall_col, new_wall_row))
        if not wall_in_boundaries:
            return False
        # - 2: is valid to place
        new_wall = Wall(new_wall_col, new_wall_row, new_wall_direction)
        if not self.is_wall_valid_to_place(new_wall):
            return False

        # add wall
        self.__walls.append(new_wall)
        return True

    def should_remove_wall(self, wall: Wall) -> bool:
        """
        Checks if the given wall is outside the board's boundaries,
        therefore should be removed
        :param wall: a wall candidate
        :return: True if the wall should be removed, False otherwise
        """
        body_index = len(wall.wall_cells) // 2
        tail_index = 0

        wall_body_in_board_boundaries = self.is_coord_in_board_boundaries(
            wall.wall_cells[tail_index].get_location())
        wall_tail_in_board_boundaries = self.is_coord_in_board_boundaries(
            wall.wall_cells[body_index].get_location())

        return not wall_body_in_board_boundaries and \
            not wall_tail_in_board_boundaries

    def remove_walls(self) -> None:
        """
        Deletes all walls which should be removed
        """
        for index in range(len(self.__walls) - 1, -1, -1):
            if self.should_remove_wall(self.__walls[index]):
                self.__walls.pop(index)

    # endregion walls
    # region apples
    def get_apples(self) -> List[BoardCell]:
        """
        Returns a list of all the apples on the board
        """
        return self.__apples

    def is_apple_valid_to_place(self, apple: BoardCell) -> bool:
        """
        Checks whether a given coordinate is currently empty on the board,
        therefore it is valid to place
        :param apple: the new apple candidate
        :return: True if the cell are empty, False otherwise
        """
        # snake position comparions
        coordinate = apple.get_location()
        if coordinate in self.snake.get_snake_cells_locations():
            return False

        # existing walls comparions
        for existing_wall in self.__walls:
            if coordinate in existing_wall.get_wall_cells_locations():
                return False

        # existing apples comparions
        for existing_apple in self.__apples:
            if coordinate == existing_apple.get_location():
                return False

        return True

    def add_apple(self) -> bool:
        """
        Adds an apple to the game
        :return: True if apple was added, False otherwise
        """
        new_apple_col, new_apple_row = game_utils.get_random_apple_data()

        # verify conditions
        # - 1: in board's boundaries
        apple_in_boundaries = self.is_coord_in_board_boundaries((
            new_apple_col, new_apple_row))
        if not apple_in_boundaries:
            return False
        # - 2: is valid to place
        new_apple = BoardCell(new_apple_col, new_apple_row, color="green")
        if not self.is_apple_valid_to_place(new_apple):
            return False

        # add apple
        self.__apples.append(new_apple)
        return True

    def remove_apple(self, apple: BoardCell) -> bool:
        """
        Removes the apple in a given coordinate from the board
        :param apple: the apple to remove
        :return: True if succeeded to find and remove the apple,
                 False otherwise
        """
        for board_apple in self.__apples:
            if apple == board_apple:
                self.__apples.remove(apple)
                return True
        return False

    # endregion apples
    # region snake
    def get_snake_cells_length(self) -> int:
        """
        Returns a list of all the snake cells on the board
        """
        return len(self.snake.get_snake_cells())

    def cut_snake_tail(self, cutting_coordinate: Tuple[int, int]) -> None:
        """
        Cuts the tail of the snake
        :param cutting_coordinate: the coordinate of the tail to cut
        :return: None
        """
        self.snake.cut_tail(cutting_coordinate)

    def is_snake_out_boundaries(self) -> bool:
        """
        Checks whther the snake collided with the board
        :return: True if the snake is out of boundaries, False otherwise
        """
        for cell in self.snake.get_snake_cells():
            if not self.is_coord_in_board_boundaries(cell.get_location()):
                return True
        return False

    def is_snake_tangled(self) -> bool:
        """
        Checks whether the snake is tangled (ate itself)
        :return: True if the snake not tangled, False otherwise
        """
        return self.snake.is_tangled()
    # endregion snake
    # endregion game objects methods


if __name__ == "__main__":
    print("This script is part of the 'Snake' board game.\nYou should run:\n"
          "> python game_display.py [optional arguments|--help]")
