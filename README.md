![Project Preview Image](https://github.com/E-RELevant/py-snake/blob/main/media/preview.png)

# py-snake (GUI)

## 📙 About the project

An implementation of the 'Snake' game.

Snake is a sub-genre of action video game where the player maneuvers the end of a growing line, often themed as a snake. The player must keep the snake from colliding with both other obstacles and itself, which gets harder as the snake lengthens. [Read more](<https://en.wikipedia.org/wiki/Snake_(video_game_genre)>).

### ⚙️ Game settings

- `Snake` is represented by three black links.
- `Apple` is represented by one, static green link.
- `Wall` is represented by three blue vertical or horizontal links, moves in a certain direction at half the speed of the snake.

In the beginning of the game, the snake's head is located in the center of the screen facing upward. Until the required amount is reached, an apple (in green color) and a wall (in blue color) are added.

### ▶️ Interactions

#### Snake eats an apple

- In the round in which the snake ate the apple, the player receives a score equal to the square root of the snake's length.
  - As an example, a snake whose length at the beginning of the current round is 8 will receive the score of ⌊√8⌋ = 2.
- Starting from the round after eating the apple, the snake's length will gradually increase by 3 links.
- A new apple is added in its place the next round.

#### A wall goes beyond the boundaries of the board

- A new wall is added in its place the next round.

#### A wall collided with the snake's body

- The snake's tail will be cut off at the point of collision.

#### Snake out of the boundaries of the board, collided with a wall or itself

- Game over.

## 🚩 Getting started

run:

```shell
> python game_display.py --help

usage: game_display.py [-h] [-x WIDTH] [-y HEIGHT] [-s SEED] [-a APPLES] [-d]
                       [-w WALLS] [-r ROUNDS] [-t DELAY] [-v]

Runs the "Snake" game. Closes the program automatically when disqualified.

optional arguments:
  -h, --help            show this help message and exit
  -x WIDTH, --width WIDTH
                        args.width: Game board width
  -y HEIGHT, --height HEIGHT
                        args.height: Game board height
  -s SEED, --seed SEED  Seed for random number generator (not passed to game loop)
  -a APPLES, --apples APPLES
                        args.apples: Number of apples
  -d, --debug           args.debug: Debug mode with no snake
  -w WALLS, --walls WALLS
                        args.walls: Number of walls
  -r ROUNDS, --rounds ROUNDS
                        args.rounds: Number of rounds
  -t DELAY, --delay DELAY
                        Delay between rounds in milliseconds (not passed to game loop)
  -v, --verbose         Print helpful debugging information (not passed to game loop, can be used multiple times)
```

### 🔎 Examples

```shell
>  python game_display.py
```

```shell
# A board with a width of 30, a height of 40, 4 apples, and 1 wall
> python game_display.py --width 30 --height 40 --apples 4 --walls 1
```

```shell
# A board with a width of 50, a height of 60, 5 apples, 2 walls, and 500 rounds
> python game_display.py -x 50 -y 60 -a 5 -w 2 -r 500
```

The program uses `tkinter`, Python's standard GUI package. If you do not
already have `tkinter`, you can install it with:

```shell
> pip install -r requirements.txt
```

## 💻 Built with

The game was built in `Python 3.9`, using the `tkinter` package ("Tk interface") GUI toolkit.

Designed and tested on Windows 11.
