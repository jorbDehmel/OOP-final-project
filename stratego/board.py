'''
This module defines the board class for an Object-Oriented
Stratego game.
'''

from typing import Union, List, Optional, Tuple
import stratego.pieces as p


class LakeSquare:
    '''
    A lake square on a Stratego board. This may not be moved
    into, and never moves. This should be left as a unit class.
    '''


class InvalidMoveError(Exception):
    '''
    An error raised by attempting to make an invalid move in
    stratego. This should be left as a unit class.
    '''


# A square on a stratego board (via typedef)
Square = Optional[Union[p.Piece, LakeSquare]]


class Board:
    '''
    A Stratego board. This should be a singleton class which
    aggregates pieces.
    '''

    _IS_INSTANTIATED: bool = False
    _WIDTH: int = 10
    _HEIGHT: int = 10

    def __init__(self) -> None:
        '''
        Constructs an empty Stratego board populated with the
        standard lake setup. This will be a 10x10 board.
        '''

        # Ensure singleton-ness
        if type(self)._IS_INSTANTIATED:
            raise ValueError('Cannot instantiate multiple boards!')

        type(self)._IS_INSTANTIATED = True

        self._places: List[List[Square]] = []

        # For each row requested
        for _ in range(type(self)._HEIGHT):

            # Create a new temp row
            row_temp: List[Square] = [None for _ in range(type(self)._WIDTH)]

            # Append the created row
            self._places.append(row_temp)

        # Add "left" lake
        self._places[5][2] = LakeSquare()
        self._places[5][3] = LakeSquare()
        self._places[6][2] = LakeSquare()
        self._places[6][3] = LakeSquare()

        # Add "right" lake
        self._places[5][6] = LakeSquare()
        self._places[5][7] = LakeSquare()
        self._places[6][6] = LakeSquare()
        self._places[6][7] = LakeSquare()

    def __repr__(self) -> str:
        '''
        Represent the board as a string.

        :returns: ASCII art of the board.
        '''

        rows: List[str] = []

        for row in self._places:
            cur_row: List[str] = [' ' for _ in row]

            for i, piece in enumerate(row):

                if isinstance(piece, LakeSquare):
                    cur_row[i] = 'L'

                elif isinstance(piece, p.Piece):
                    cur_row[i] = str(piece)

            rows.append('|' + ''.join(cur_row) + '|\n')

        top: str = '+' + ('-' * type(self)._WIDTH) + '+\n'
        out: str = top + ''.join(rows) + top
        return out

    def move(self,
             color: str,
             from_pair: Tuple[int, int],
             to_pair: Tuple[int, int]) -> str:
        '''
        Attempts to move from the given coordinates to the given
        coordinates. Raises error if the move is invalid. If
        the move was valid, updates the board accordingly.

        :param from_pair: The origin (x, y).
        :param to_pair: The destination (x, y).
        :returns: The game state.
        '''

        from_x, from_y = from_pair
        to_x, to_y = to_pair

        # This succeeding implies that temp is of type Piece
        if not self.__is_valid_move(from_x, from_y, to_x, to_y):
            raise InvalidMoveError('Failed to make move')

        s: Square = self._places[from_y][from_x]
        t: Square = self._places[to_y][to_y]
        if isinstance(s, p.Piece) and isinstance(t, p.Piece):

            # We have to put all this in the if statement due
            # to Python's stupid typing.

            mover: p.Piece = s
            defender: p.Piece = t

            self._places[to_y][to_x] = mover.confront(defender)

            if isinstance(self._places[to_y][to_x], p.Flag):
                return color

            return 'GOOD'

        raise InvalidMoveError('Failure in move checking algorithm')

    @classmethod
    def __move_is_inside_board(cls,
                               from_x: int,
                               to_x: int,
                               from_y: int,
                               to_y: int) -> bool:
        '''
        Returns true if an only if the given parameters fall
        within the board.

        :param from_x: The origin x.
        :param to_x: The destination x.
        :param from_y: The origin y.
        :param to_y: The destination y.
        :returns: Whether the moves fall within the board.
        '''

        # Cannot move piece from outside board
        if cls._WIDTH < from_x or cls._WIDTH < to_x:
            return False

        # Cannot move piece to outside board
        if cls._HEIGHT < from_y or cls._HEIGHT < to_y:
            return False

        # Cannot move to negative index
        if from_x < 0 or to_x < 0 or from_y < 0 or to_y < 0:
            return False

        return True

    @staticmethod
    def __move_is_logical(from_x: int,
                          to_x: int,
                          from_y: int,
                          to_y: int) -> bool:
        '''
        Returns true if the move adheres to the general
        rules of stratego movement- Namely that you cannot
        move diagonally and you must move some amount.

        :param from_x: The origin x.
        :param to_x: The destination x.
        :param from_y: The origin y.
        :param to_y: The destination y.
        :returns: False if this move is invalid.
        '''

        # Cannot move diagonally
        if from_x != to_x and from_y != to_y:
            return False

        # Must move
        if from_x == to_x and from_y == to_y:
            return False

        return True

    @staticmethod
    def __types_are_legal(from_piece: Square, to_piece: Square) -> bool:
        '''
        Checks whether the types are legal.

        :param from_piece: The square to be moved.
        :param to_piece: The square to be moved onto.
        :returns: False if this move is invalid.
        '''

        # Cannot move nothing
        if from_piece is None:
            return False

        # Ok if destination is nothing
        if to_piece is None:
            return True

        # Cannot move lake, bomb, or flag
        if isinstance(from_piece, (LakeSquare, p.Bomb, p.Flag)):
            return False

        # Cannot move into lake
        if isinstance(to_piece, LakeSquare):
            return False

        # Cannot move onto own piece
        if from_piece.color == to_piece.color:
            return False

        return True

    def __move_makes_sense_for_type(self,
                                    from_x: int,
                                    to_x: int,
                                    from_y: int,
                                    to_y: int) -> bool:
        '''
        Checks whether this move makes sense for this type.

        :returns: False if this move is invalid.
        '''

        # Cannot move a scout through other pieces
        if isinstance(self._places[from_y][from_x], p.Scout):

            # If moving in the x-direction
            if from_x - to_x != 0:
                x_step: int = 1 if to_x > from_x else -1

                for x in range(from_x + x_step, to_x, x_step):
                    if self._places[from_y][x] is not None:
                        return False

            # If moving in the x-direction
            else:
                y_step: int = 1 if to_y > from_y else -1

                for y in range(from_y + y_step, to_y, y_step):
                    if self._places[y][from_x] is not None:
                        return False

        # Cannot move a non-scout more than one square
        else:
            if abs(from_x - to_x) > 1:
                return False

            if abs(from_y - to_y) > 1:
                return False

        return True

    def __is_valid_move(self,
                        from_x: int,
                        from_y: int,
                        to_x: int,
                        to_y: int) -> bool:
        '''
        Returns true if the given move is valid, false
        otherwise.

        :returns: True if the move is valid, False otherwise.
        '''

        if not (self.__move_is_inside_board(from_x, to_x, from_y, to_y)
                and self.__move_is_logical(from_x, to_x, from_y, to_y)):
            return False

        from_piece: Square = self._places[from_y][from_x]
        to_piece: Square = self._places[to_y][to_x]

        # Final checks
        return (self.__types_are_legal(from_piece, to_piece)
                and self.__move_makes_sense_for_type(from_x,
                to_x, from_y, to_y))
