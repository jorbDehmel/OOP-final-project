'''
This module defines the board class for an Object-Oriented
Stratego game.
'''

from typing import Union, List, Optional, Tuple, Literal, Callable
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

    __INSTANCE: Optional['Board'] = None
    _WIDTH: int = 10
    _HEIGHT: int = 10

    @classmethod
    def clear_instance(cls) -> None:
        '''
        Resets this singleton class.
        '''

        if cls.__INSTANCE is not None:
            del cls.__INSTANCE
            cls.__INSTANCE = None

    @classmethod
    def get_instance(cls) -> 'Board':
        '''
        Returns the instance of this class, instantiating if
        necessary.
        :returns: The board.
        '''

        if cls.__INSTANCE is None:
            cls.__INSTANCE = Board()

        return cls.__INSTANCE

    def __init__(self) -> None:
        '''
        Constructs an empty Stratego board populated with the
        standard lake setup. This will be a 10x10 board.
        '''

        # Ensure singleton-ness
        if type(self).__INSTANCE is not None:
            raise ValueError('Cannot instantiate multiple boards!')

        type(self).__INSTANCE = self

        self._places: List[List[Square]] = []

        # For each row requested
        for _ in range(type(self)._HEIGHT):

            # Create a new temp row
            row_temp: List[Square] = [None for _ in range(type(self)._WIDTH)]

            # Append the created row
            self._places.append(row_temp)

        # Add "left" lake
        self._places[4][2] = LakeSquare()
        self._places[4][3] = LakeSquare()
        self._places[5][2] = LakeSquare()
        self._places[5][3] = LakeSquare()

        # Add "right" lake
        self._places[4][6] = LakeSquare()
        self._places[4][7] = LakeSquare()
        self._places[5][6] = LakeSquare()
        self._places[5][7] = LakeSquare()

    @staticmethod
    def all_pieces(color: Literal['RED', 'BLUE']) -> List[p.Piece]:
        '''
        Returns all 40 pieces which need to be placed at game
        setup.
        :returns: A list of all 40 needed pieces.
        '''

        return ([p.Bomb(color)] * 6
                + [p.Scout(color)] * 8
                + [p.Miner(color)] * 5
                + [p.Marshal(color),
                    p.Spy(color),
                    p.Flag(color),
                    p.Troop(color, 9),
                    p.Troop(color, 8),
                    p.Troop(color, 8)]
                + [p.Troop(color, 7)] * 3
                + [p.Troop(color, 6),
                    p.Troop(color, 5),
                    p.Troop(color, 4)] * 4)

    @property
    def height(self) -> int:
        '''
        :return: The board height.
        '''

        return self._HEIGHT

    @property
    def width(self) -> int:
        '''
        :return: The board width.
        '''

        return self._WIDTH

    def clear(self) -> None:
        '''
        Erase all pieces from the board.
        '''

        self.fill((0, 0), (self._WIDTH, self._HEIGHT), None)

    def fill(self,
             start: Tuple[int, int],
             end: Tuple[int, int],
             to: Union[Square, Callable[[int, int], Square]]) -> None:
        '''
        Sets every item in the given range to the given square.
        :param start: A 2-tuple for the starting (x, y).
        :param end: A 2-tuple for the ending (x, y).
        :param to: The item to set each square in the range to.
            This can also be a callable, in which case the
            object copied will be to(x, y) for each (x, y) in
            the range.
        '''

        if to is None or isinstance(to, (p.Piece, LakeSquare)):
            for y in range(start[1], end[1]):
                for x in range(start[0], end[0]):
                    self._places[y][x] = to

        else:
            for y in range(start[1], end[1]):
                for x in range(start[0], end[0]):
                    self._places[y][x] = to(x, y)

    def get(self, x: int, y: int) -> Square:
        '''
        Get the piece at the given point.

        :param x: The x position.
        :param y: The y position.
        '''

        if x >= self._WIDTH or y >= self._HEIGHT:
            return None

        if x < 0 or y < 0:
            return None

        return self._places[y][x]

    def set_piece(self, x: int, y: int, what: Square) -> None:
        '''
        Set the piece at the given point.

        :param x: The x position.
        :param y: The y position.
        :param what: The item to set.
        '''

        if x >= self._WIDTH or y >= self._HEIGHT:
            raise ValueError('Invalid dimension')

        if x < 0 or y < 0:
            raise ValueError('Invalid dimension')

        self._places[y][x] = what

    def move(self,
             color: Literal['BLUE', 'RED'],
             from_pair: Tuple[int, int],
             to_pair: Tuple[int, int]) -> Literal['RED', 'BLUE', 'GOOD']:
        '''
        Attempts to move from the given coordinates to the given
        coordinates. Raises error if the move is invalid. If
        the move was valid, updates the board accordingly.

        Note: Can only return 'GOOD' or `color`; It never
        returns the other color.

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

        if isinstance(s, p.Piece):
            if s.color != color:
                raise InvalidMoveError('Failed to make move')

        t: Square = self._places[to_y][to_x]
        if isinstance(s, p.Piece) and isinstance(t, p.Piece):

            # We have to put all this in the if statement due
            # to Python's stupid typing.

            mover: p.Piece = s
            defender: p.Piece = t

            self._places[to_y][to_x] = mover.confront(defender)
            self._places[from_y][from_x] = None

            if isinstance(self._places[to_y][to_x], p.Flag):
                return color

            return 'GOOD'

        self._places[to_y][to_x] = self._places[from_y][from_x]
        self._places[from_y][from_x] = None
        return 'GOOD'

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

        # Cannot move lake, bomb, or flag
        if isinstance(from_piece, (LakeSquare, p.Bomb, p.Flag)):
            return False

        # Cannot move into lake
        if isinstance(to_piece, LakeSquare):
            return False

        # Cannot move onto own piece
        if to_piece is not None and from_piece.color == to_piece.color:
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

            # If moving in the y-direction
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
