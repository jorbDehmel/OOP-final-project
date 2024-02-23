'''
Tests the `Piece` classes for OOP Stratego.
'''

from typing import Optional
from stratego import pieces as p


def test_bomb() -> None:
    '''
    Test the bomb class for Stratego pieces. This should pass if
    and only if the interactions between bombs, regular pieces,
    and miners are correct.
    '''

    # Create a bomb and a regular troop
    bomb: p.Bomb = p.Bomb()
    troop: p.Troop = p.Troop(5)

    # Simulate an interaction between the two
    result: Optional[p.Piece] = troop.confront(bomb)
    assert result is None

    # Simulate an interaction between a miner and a bomb
    miner: p.Miner = p.Miner()
    result = miner.confront(bomb)
    assert result is miner


def test_flag() -> None:
    '''
    '''


def test_spy() -> None:
    '''
    '''


def test_scout() -> None:
    '''
    '''


def test_miner() -> None:
    '''
    '''


def test_marshal() -> None:
    '''
    '''


def test_troop() -> None:
    '''
    '''


def test_confrontation_1() -> None:
    '''
    '''


def test_confrontation_2() -> None:
    '''
    '''


def test_confrontation_3() -> None:
    '''
    '''


def test_confrontation_4() -> None:
    '''
    '''


def test_confrontation_5() -> None:
    '''
    '''
