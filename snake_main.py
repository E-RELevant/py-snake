"""
FILE: snake_main.py
DESCRIPTION: the manager of the 'snake' game. Contains the main loop of the
game.
"""
###############################################################################
#                                   Imports                                   #
###############################################################################
import math
import argparse
from typing import Optional, Tuple
from board import Board
from game_display import GameDisplay


###############################################################################
#                                  Functions                                  #
###############################################################################
# region interactions
def interaction_snake_walls(board: Board) -> \
        Tuple[bool, Optional[Tuple[int, int]]]:
    """
    Cuts the snake from the tip of the tail to the cutting point
    :param board: a Board object
    :return: None
    """
    collision_bool, hit_location = is_snake_cut_by_wall(board)

    if collision_bool:
        assert hit_location is not None
        if len(board.snake.get_snake_cells()) < 1:
            board.is_over = True
        if board.snake.compare_to_head(hit_location):
            board.is_over = True

    return collision_bool, hit_location


def is_snake_cut_by_wall(board: Board) -> \
        Tuple[bool, Optional[Tuple[int, int]]]:
    """
    Checks whether the snake has been cut by a wall
    :return: Tuple[True, (column, row)] if the snake was cut by a wall,
             Tuple[False, None] otherwise.
    """
    for wall in board.get_walls():
        collision, location = board.snake.is_collided(wall.wall_cells)
        if collision:
            return collision, location

    return False, None


def interaction_snake_apples(board: Board) -> None:
    """
    Checks whether the snake's head is in the same position as an apple.
    In that case, removes the apple from the board, updates the game
    score, and increase the snake's length
    :param board: a Board object
    :return: None
    """
    for apple in board.get_apples():
        if board.snake.compare_to_head(apple.get_location()):
            board.remove_apple(apple)
            board.snake.grow()
            score_calculation = math.floor(board.snake.get_length() ** 0.5)
            board.increase_score(score_calculation)


def interaction_walls_apples(board: Board) -> None:
    """
    Checks whether an apple got 'crashed' by a wall. If so, removes the apple
    :param board: a Board object
    :return: None
    """
    for apple in board.get_apples():
        for wall in board.get_walls():
            if apple.get_location() in wall.get_wall_cells_locations():
                board.remove_apple(apple)


# endregion interactions

def main_loop(gd: GameDisplay, args: argparse.Namespace) -> None:
    """
    The main loop of the snake game
    :param gd: a GameDisplay
    :param args: the arguments of the 'snake game'
    :return: None
    """
    # region round 0
    # init objects
    board = Board(is_debug=args.debug)
    gd.show_score(board.get_score())

    # add outside the board's boundaries objects
    if len(board.get_walls()) < int(args.walls):
        board.add_wall()
    if len(board.get_apples()) < int(args.apples):
        board.add_apple()

    # draw board
    board.draw_board(gd)

    # end round
    gd.end_round()
    # endregion round 0

    while not board.is_over and args.rounds != 0:
        # add round count
        board.add_round()

        # check key press
        key_clicked = gd.get_key_clicked()
        board.read_key(key_clicked)

        # update moving objects
        board.update_moving_objects()

        # apples' interactions
        interaction_walls_apples(board)
        if not args.debug:
            interaction_snake_apples(board)

        # check for new objects to add
        if len(board.get_walls()) < int(args.walls):
            board.add_wall()
        if len(board.get_apples()) < int(args.apples):
            board.add_apple()

        # update score
        gd.show_score(board.get_score())

        # draw board
        board.draw_board(gd)

        # wait for next round
        gd.end_round()

        # tangled snake
        if not args.debug:
            # cut the snake after collision (next turn)
            cut_tail, cutting_point = interaction_snake_walls(board)
            if cut_tail:
                assert cutting_point is not None
                board.cut_snake_tail(cutting_point)
                # check whether only the head remained
                if board.get_snake_cells_length() <= 1:
                    board.is_over = True

        # conditions to verify
        # - 1: no more rounds
        is_rounds_over = 0 < args.rounds < board.get_rounds() + 1
        # - 2: the snake is oudside the board's boundaries
        is_snake_out_bounds = board.is_snake_out_boundaries() if not \
            args.debug else False
        # - 3: the snake is tangled
        is_snake_tangled = not board.is_snake_tangled() if not args.debug \
            else False

        if (is_rounds_over or is_snake_out_bounds or is_snake_tangled) and \
                not board.is_over:
            board.is_over = True


if __name__ == "__main__":
    print("This script is part of the 'Snake' board game.\nYou should run:\n"
          "> python game_display.py [optional arguments|--help]")
