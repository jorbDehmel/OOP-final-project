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

    def confront(self, other: Piece) -> Optional[Piece]:
        '''
        A confrontation between another piece and this one.

        :returns: The winning piece.
        '''

        if repr(other) == '3':
            return other

        return self


class Troop(Piece):
    '''
    A standard, non-special Stratego piece; This has no special
    properties, just a rank.
    '''

    def __init__(self, rank: int) -> None:
        '''
        Initializes a new non-special ranked troop w/ the given
        rank value.
        '''

        self.__rank = rank

    def confront(self, other: Piece) -> Optional[Piece]:
        '''
        Pit this item against another.
        '''

    def __repr__(self) -> str:
        '''
        Returns a string representation of this object.
        :returns: The string representing this object.
        '''

        return str(self.__rank)


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

    def confront(self, other: Piece) -> Optional[Piece]:
        '''
        A confrontation between another piece and this one.

        :returns: The winning piece.
        '''

        return self


class Spy(Troop):
    '''
    A Stratego piece which can kill marshals.
    '''

    def __init__(self) -> None:
        '''
        Create this piece by calling the superclass constructor.
        '''

        super().__init__(1)


class Scout(Troop):
    '''
    A Stratego piece which can move any number of places instead
    of just 1 per turn, possible attacking on the same turn as
    moving.
    '''

    def __init__(self) -> None:
        '''
        Create this piece by calling the superclass constructor.
        '''

        super().__init__(2)


class Miner(Troop):
    '''
    A Stratego piece which can diffuse bombs.
    '''

    def __init__(self) -> None:
        '''
        Create this piece by calling the superclass constructor.
        '''

        super().__init__(3)

    def confront(self, other: Piece) -> Optional[Piece]:
        '''
        A confrontation between another piece and this one.

        :returns: The winning piece.
        '''

        if repr(other) == 'B':
            return self

        return super().confront(other)


class Marshal(Troop):
    '''
    A Stratego piece which can only be killed by spies.
    '''

    def __init__(self) -> None:
        '''
        Create this piece by calling the superclass constructor.
        '''

        super().__init__(10)
