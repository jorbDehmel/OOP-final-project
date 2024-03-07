'''
This module defines the board class for an Object-Oriented
Stratego game.
'''

from typing import Union, List, Optional
import stratego.pieces as p


class LakeSquare:
    '''
    A lake square on a Stratego board. This may not be moved
    into.
    '''


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
