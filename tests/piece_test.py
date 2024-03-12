'''
Tests the `Piece` classes for OOP Stratego.
'''

from typing import Optional
from unittest import TestCase
from stratego import pieces as p


class TestStratego(TestCase):
    '''
    A test case for stratego, inheriting from the
    unittest.TestCase class.
    '''

    def test_bomb(self) -> None:
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

    def test_flag(self) -> None:
        '''
        Tests the flag piece for stratego. This should pass if and
        only if the interactions between all pieces are correct. A
        flag will be returned no matter what confronts it. However,
        a flag will never confront anything, since it cannot move.
        The player who confronts the opponent's flag wins.
        '''

    def test_spy(self) -> None:
        '''
        Tests the spy piece for stratego. The spy should be killed
        by everything except a marshal, which it will defeat.
        '''

    def test_scout(self) -> None:
        '''
        Tests the scout piece for stratego. The scout piece is able
        to move any number of spaces, instead of just one.
        '''

    def test_miner(self) -> None:
        '''
        Tests the miner piece for stratego. The miner is able to
        defuse bombs.
        '''

    def test_marshal(self) -> None:
        '''
        Tests the marshal piece for stratego. The marshal is the
        highest rank (10), but is killed by spies and bombs.
        '''

    def test_troop(self) -> None:
        '''
        Tests an arbitrary troop (IE not one of the above special
        cases). These all use standard rules with no special cases.
        '''

    def test_confrontation(self) -> None:
        '''
        Tests random confrontations between arbitrary pieces using
        the hypothesis library.
        '''
