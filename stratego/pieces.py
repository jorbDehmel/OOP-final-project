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

    def __init__(self):
        '''
        Constructs a Stratego piece.
        '''

        raise TypeError('Cannot call method on abstract base class!')

    def __repr__(self):
        '''
        Returns a unique identifying char of this piece.

        :returns: A single char representing this piece.
        '''

        raise TypeError('Cannot call method on abstract base class!')

    def confront(self, other: "Piece") -> Optional["Piece"]:
        '''
        Move this piece onto the other. This will return the
        piece which is the "winner". If the other piece is a
        bomb, this will return None.

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


class Troop(Piece):
    '''
    A standard, non-special Stratego piece; This has no special
    properties, just a rank.
    '''


class Flag(Troop):
    '''
    A Stratego piece which ends the game if captured.
    '''


class Spy(Troop):
    '''
    A Stratego piece which can kill marshals.
    '''


class Scout(Troop):
    '''
    A Stratego piece which can move any number of places instead
    of just 1 per turn, possible attacking on the same turn as
    moving.
    '''


class Miner(Troop):
    '''
    A Stratego piece which can diffuse bombs.
    '''


class Marshal(Troop):
    '''
    A Stratego piece which can only be killed by spies.
    '''
