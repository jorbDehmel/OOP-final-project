'''
This module defines classes for an Object-Oriented Stratego
game.
'''

from abc import ABC, abstractmethod
from typing import Optional, Literal


class Piece(ABC):
    '''
    A Stratego piece. This should be an abstract base class
    which is inherited by specific pieces.
    '''

    def __init__(self, color: Literal['BLUE', 'RED']) -> None:
        '''
        A base constructor for a stratego piece. Must take the
        color of the piece.

        :param color: Either 'RED' or 'BLUE'.
        '''

        self.__color: str = color

    @abstractmethod
    def __repr__(self) -> str:
        '''
        Returns a unique identifying char of this piece.

        :returns: A single char representing this piece.
        '''

    @abstractmethod
    def confront(self, other: "Piece") -> Optional["Piece"]:
        '''
        Move this piece onto the other. This will return the
        piece which is the "winner".

        :param other: The piece which was already on this
            square.
        :returns: Either self if the other was defeated, other
            if self was defeated, None if both are defeated. If
            the other is a flag, always returns it.
        '''

    @property
    def color(self) -> str:
        '''
        Gets the color of this piece.

        :returns: This piece's color.
        '''

        return self.__color


class Bomb(Piece):
    '''
    A Stratego piece which can defeat all others except for
    miners.
    '''

    def __repr__(self) -> str:
        '''
        Returns a string representation of this object.
        :returns: The string representing this object.
        '''

        return 'B'

    def confront(self, _: Piece) -> Optional[Piece]:
        '''
        A dummy implementation to prevent this from being an
        ABC. Never returns anything, since this should never be
        called.
        '''

        raise TypeError('Bombs are not able to move; How did you do this?')


class Troop(Piece):
    '''
    A standard, non-special Stratego piece; This has no special
    properties, just a rank. If confront is called here, it is
    assumed that the caller has no special properties. However,
    the piece being confronted might.
    '''

    def __init__(self, color: Literal['BLUE', 'RED'], rank: int) -> None:
        '''
        Initializes a new non-special ranked troop w/ the given
        rank value.

        :param color: Either 'RED' or 'BLUE'
        '''

        super().__init__(color)
        self.__rank = rank

    def confront(self, other: Optional[Piece]) -> Optional[Piece]:
        '''
        Pit this item against another.
        '''

        if other is None:
            return self

        if isinstance(other, (Bomb, Flag)):
            return other

        if isinstance(other, Troop) and self.__rank < other.rank:
            return other

        if isinstance(other, Troop) and self.__rank == other.rank:
            return None

        return self

    def __repr__(self) -> str:
        '''
        Returns a string representation of this object.
        :returns: The string representing this object.
        '''

        return str(self.__rank)

    @property
    def rank(self) -> int:
        '''
        Return this piece's rank.

        :returns: Rank.
        '''

        return self.__rank


class Flag(Piece):
    '''
    A Stratego piece which ends the game if captured.
    '''

    def __repr__(self) -> str:
        '''
        Returns a string representation of this object.
        :returns: The string representing this object.
        '''

        return 'F'

    def confront(self, _: Piece) -> Optional[Piece]:
        '''
        A dummy implementation to prevent this from being an
        ABC. Never returns anything, since this should never be
        called.
        '''

        raise TypeError('Bombs are not able to move; How did you do this?')


class Spy(Troop):
    '''
    A Stratego piece which can kill marshals.
    '''

    def __init__(self, color: Literal['BLUE', 'RED']) -> None:
        '''
        Create this piece by calling the superclass constructor.

        :param color: Either 'RED' or 'BLUE'
        '''

        super().__init__(color, 1)

    def confront(self, other: Optional[Piece]) -> Optional[Piece]:
        '''
        A confrontation between another piece and this one.

        :returns: The winning piece.
        '''

        if isinstance(other, Marshal):
            return self

        return super().confront(other)


class Scout(Troop):
    '''
    A Stratego piece which can move any number of places instead
    of just 1 per turn, possible attacking on the same turn as
    moving.
    '''

    def __init__(self, color: Literal['BLUE', 'RED']) -> None:
        '''
        Create this piece by calling the superclass constructor.

        :param color: Either 'RED' or 'BLUE'
        '''

        super().__init__(color, 2)


class Miner(Troop):
    '''
    A Stratego piece which can diffuse bombs.
    '''

    def __init__(self, color: Literal['BLUE', 'RED']) -> None:
        '''
        Create this piece by calling the superclass constructor.

        :param color: Either 'RED' or 'BLUE'
        '''

        super().__init__(color, 3)

    def confront(self, other: Optional[Piece]) -> Optional[Piece]:
        '''
        A confrontation between another piece and this one.

        :returns: The winning piece.
        '''

        if isinstance(other, Bomb):
            return self

        return super().confront(other)


class Marshal(Troop):
    '''
    A Stratego piece which can only be killed by spies.
    '''

    def __init__(self, color: Literal['BLUE', 'RED']) -> None:
        '''
        Create this piece by calling the superclass constructor.

        :param color: Either 'RED' or 'BLUE'.
        '''

        super().__init__(color, 10)
