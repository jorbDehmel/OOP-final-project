
![GitHub Actions CI/CD](https://github.com/jorbDehmel/OOP-final-project/actions/workflows/ci-test.yml/badge.svg)

# OOP-final-project

Final project for object oriented programming w/ Dr. Ram Basnet.

## Authors

Nate Barnaik \
Jordan Dehmel \
Kate Eckhart \

# Abstract

Stratego is a board game in which two players command an
army to try and capture the opposing player's flag or defeat
every moveable piece.  Each player’s army has 40 pieces that
they place on their side of the board as they please, with each
piece having a different rank and some pieces having special
abilities like full movement in one direction.  When a piece
attacks another piece, the piece with the lower rank is removed
from the board, if the ranks are the same then both pieces are
removed from the board.  Exceptions are the Spy which can remove
the Marshal, Bombs which can remove anything that attacks them,
except Miners who are the only piece that can remove bombs. All
of these rules can be done by setting up a base piece class
which has child classes for each piece type.  PyGame can be of
help when displaying the game to the player, and object-based
Python networking can be used for multiplayer. This project
outlines the construction of an Object-Oriented Python
implementation of Stratego.

# Outline

## Pieces Per Player

Rank | Name    | Count | Properties
-----|---------|-------|----------------------------------------
10   | Marshal    | 1     | Killed by spies
9    | General    | 1     |
8    | Colonel    | 2     |
7    | Major      | 3     |
6    | Captain    | 4     |
5    | Lieutenant | 4     |
4    | Sergeant   | 4     |
3    | Miner      | 5     | Can defuse bombs
2    | Scout      | 8     | Moves any number of spaces
1    | Spy        | 1     | Kills marshals
F    | Flag       | 1     | Win condition
B    | Bomb       | 6     | Kills all non-miners

## Board

![A stratego board.](images/board.jpg)

## Rules

- You can only see your own pieces.
- Pieces are set up at the beginning.
- Each player begins with the pieces specified above.
- Pieces are set up in any orientation of 4x10.
- Bombs and flags cannot move.
- Most pieces can move (non-diagonally) one space per turn.
- Pieces cannot move into lake spaces.
- If a piece advances into a piece of the opposite color, it is
    a challenge. Whichever piece is of lower rank will be
    removed from play, unless a special case occurs. If the
    piece which was moved into is a flag, the moving piece's
    side wins. If it was a bomb, both pieces are removed unless
    a special case occurs.
- If a "miner" (rank 3) challenges a bomb, the bomb is
    "diffused" and removed from play.
- If a spy and a marshal are involved in a challenge, the
    marshal is removed from play.
- Red plays first.
- Scouts can move any number of spaces horizontally or
    vertically in a single turn, optionally challenging a piece
    in the same turn.

## Project 4+1 Diagrams

Development: \
![Development view](4+1_view/development.png)

Logical: \
![Logical view](4+1_view/logical.png)

Physical: \
![Physical view](4+1_view/physical.png)

Process: \
![Process view](4+1_view/process.png)

Scenarios: \
![Scenarios view](4+1_view/scenarios.png)

## Attribution
Please enter what you have done below.

Nate Barnaik:
 - foobar

Jordan Dehmel:
 - foobar

Kate Eckhart:
 - foobar
