'''
This module defines classes for an Object-Oriented Stratego
game.
'''

from typing import Optional


class Piece:
    '''
    A Stratego piece. This should be an abstract base class
    which is inherited by specific pieces.
    '''

    def __init__(self, color: str) -> None:
        '''
        A base constructor for a stratego piece. Must take the
        color of the piece.

        :param color: Either 'RED' or 'BLUE'.
        '''

        self.__color = color

        if self.__color not in ('RED', 'BLUE'):
            raise ValueError('Piece color must be either "RED" or "BLUE"')

    def __repr__(self) -> str:
        '''
        Returns a unique identifying char of this piece.

        :returns: A single char representing this piece.
        '''

        raise TypeError('Cannot call method on abstract base class!')

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

        raise TypeError('Cannot call method on abstract base class!')

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


class Troop(Piece):
    '''
    A standard, non-special Stratego piece; This has no special
    properties, just a rank. If confront is called here, it is
    assumed that the caller has no special properties. However,
    the piece being confronted might.
    '''

    def __init__(self, color: str, rank: int) -> None:
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


class Spy(Troop):
    '''
    A Stratego piece which can kill marshals.
    '''

    def __init__(self, color: str) -> None:
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

        if other is None:
            return self

        if isinstance(other, Marshal):
            return self

        return other


class Scout(Troop):
    '''
    A Stratego piece which can move any number of places instead
    of just 1 per turn, possible attacking on the same turn as
    moving.
    '''

    def __init__(self, color: str) -> None:
        '''
        Create this piece by calling the superclass constructor.

        :param color: Either 'RED' or 'BLUE'
        '''

        super().__init__(color, 2)


class Miner(Troop):
    '''
    A Stratego piece which can diffuse bombs.
    '''

    def __init__(self, color: str) -> None:
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

        if other is None:
            return self

        if isinstance(other, Bomb):
            return self

        return super().confront(other)


class Marshal(Troop):
    '''
    A Stratego piece which can only be killed by spies.
    '''

    def __init__(self, color: str) -> None:
        '''
        Create this piece by calling the superclass constructor.

        :param color: Either 'RED' or 'BLUE'.
        '''

        super().__init__(color, 10)

    def confront(self, other: Optional[Piece]) -> Optional[Piece]:
        '''
        A confrontation between another piece and this one.

        :returns: The winning piece.
        '''

        if other is None:
            return self

        if isinstance(other, Troop) and other.rank == 1:
            return other

        return super().confront(other)
