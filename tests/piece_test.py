'''
Tests the `Piece` classes for OOP Stratego.
'''

from typing import Optional, List, TypeAlias, Iterable
from unittest import TestCase
from stratego import pieces as p
from stratego import board as b

def base_all_pieces(color: str) -> Iterable[p.Piece]:
    yield p.Flag(color)
    yield p.Spy(color)
    yield p.Scout(color)
    yield p.Miner(color)
    for i in range(4, 10):
        yield p.Troop(color, i)
    yield p.Marshal(color)

def all_pieces(color: str, *, but: set[p.Piece] = set())-> Iterable[p.Piece]:
    for piece in base_all_pieces(color):
        if piece not in but:
            yield piece

def all_movable_pieces(color: str, *, but: set[p.Piece] = set()) -> Iterable[p.Piece]:
    return all_pieces(color, but = {p.Flag(color), p.Bomb(color)} | but)

def assert_confront(lhs: p.Piece, rhs: p.Piece, expected: p.Piece):
    if not isinstance(lhs, p.Troop):
        return

    assert lhs.confront(rhs) is expected

class TestStrategoPiece(TestCase):
    '''
    A test case for stratego, inheriting from the
    unittest.TestCase class.
    '''

    def test_piece(self) -> None:
        '''
        Tests attributes of the piece class which are not
        otherwise covered.
        '''

        with self.assertRaises(ValueError):
            p.Piece('foobar')

        with self.assertRaises(TypeError):
            repr(p.Piece('RED'))

        with self.assertRaises(TypeError):
            p.Piece('RED').confront(p.Piece('BLUE'))

        self.assertEqual(p.Piece('RED').color, 'RED')
        self.assertEqual(p.Piece('BLUE').color, 'BLUE')

        for lhs_color in ["RED", "BLUE"]:
            for rhs_color in ["RED", "BLUE"]:
                pieces_lhs = list(all_pieces(lhs_color))
                pieces_rhs = list(all_pieces(rhs_color))
                for (i, lhs_piece) in enumerate(pieces_lhs):
                    for (j, rhs_piece) in enumerate(pieces_rhs):
                        expected = i == j and lhs_color == rhs_color
                        actual = lhs_piece == rhs_piece
                        self.assertEqual(expected, actual)
                        if actual:
                            self.assertEqual(hash(lhs_piece), hash(rhs_piece))

    def test_bomb(self) -> None:
        '''
        Test the bomb class for Stratego pieces. This should pass if
        and only if the interactions between bombs, regular pieces,
        and miners are correct.
        '''

        # Create a bomb
        bomb: p.Bomb = p.Bomb('RED')

        self.assertEqual(repr(bomb), 'B')

        # Simulate an interaction between a miner and a bomb
        miner: p.Miner = p.Miner('BLUE')
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

        flag = p.Flag('RED')

        for movable in all_movable_pieces('BLUE'):
            assert movable.confront(flag) is flag

    def test_troop(self) -> None:
        '''
        Tests troops. All troops should both die when confronting themselves.
        Except for Bomb+Miner and Spy+Marshal, the one with the higher rank wins.
        '''

        red_pieces = list(all_pieces('RED'))
        blue_pieces = list(all_pieces('BLUE'))

        inverted_winners = {frozenset({p.Bomb, p.Miner}), frozenset({p.Spy, p.Marshal})}

        for red_piece in red_pieces:
            if type(red_piece) not in {p.Troop, p.Scout}:
                continue
            for blue_piece in blue_pieces:
                red_rank = red_piece.rank
                blue_rank = blue_piece.rank
                if {type(red_piece), type(blue_piece)} in inverted_winners:
                    continue
                if red_rank < blue_rank:
                    assert_confront(red_piece, blue_piece, blue_piece)
                    assert_confront(blue_piece, red_piece, blue_piece)
                elif red_rank > blue_rank:
                    assert_confront(red_piece, blue_piece, red_piece)
                    assert_confront(blue_piece, red_piece, red_piece)
                else: # red_rank == blue_rank
                    assert_confront(red_piece, blue_piece, None)
                    assert_confront(blue_piece, red_piece, None)


    def test_spy_marshal(self) -> None:
        '''
        Tests the spy piece for stratego. The spy should be killed
        by everything except a marshal, which it will defeat.
        '''

        spy = p.Spy('RED')

        marshal = p.Marshal('BLUE')

        assert spy.confront(marshal) is spy
        assert marshal.confront(spy) is marshal

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
