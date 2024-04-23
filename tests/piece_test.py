'''
Tests the `Piece` classes for OOP Stratego.
'''

from typing import Optional, List, Iterable, Literal
from unittest import TestCase
from stratego import pieces as p


def base_all_pieces(color: str) -> Iterable[p.Piece]:
    '''
    Generator yielding all the valid pieces.
    :param color: The color to use to create.
    :yields: An iterator of pieces to use.
    '''

    yield p.Flag(color)
    yield p.Spy(color)
    yield p.Bomb(color)
    yield p.Scout(color)
    yield p.Miner(color)
    for i in range(4, 10):
        yield p.Troop(color, i)
    yield p.Marshal(color)


def all_pieces(color: Literal['RED', 'BLUE'],
               but: Optional[set[p.Piece]] = None) -> Iterable[p.Piece]:
    '''
    Yields an iterable of pieces.
    :param color: RED or BLUE.
    :param but: Pieces to exclude.
    :yields: An iterator of the given pieces.
    '''

    if but is None:
        but = set()

    for piece in base_all_pieces(color):
        if piece not in but:
            yield piece


def all_movable_pieces(color: Literal['RED', 'BLUE'],
                       but: Optional[set[p.Piece]] = None
                       ) -> Iterable[p.Piece]:
    '''
    Yields a list of only movable pieces.
    :param color: RED or BLUE.
    :param but: Pieces to exclude.
    :yields: An iterable over the given pieces.
    '''

    if but is None:
        but = set()

    return all_pieces(color, but=({p.Flag(color), p.Bomb(color)} | but))


def assert_confront(lhs: p.Piece,
                    rhs: p.Piece,
                    expected: p.Piece) -> None:
    '''
    Asserts that lhs.confront(rhs) is expected.
    :param lhs: The attacker.
    :param rhs: The defender.
    :param expected: The expected victor.
    '''

    if not isinstance(lhs, p.Troop):
        return

    assert lhs.confront(rhs) is expected


def assert_confrontation_detailed(via: TestCase,
                                  attacker: p.Piece,
                                  defender: p.Piece) -> None:
    '''
    Assert that the correct result occurs given two
    pieces.
    '''

    result: Optional[p.Piece] = attacker.confront(defender)

    repr(attacker)
    repr(defender)
    repr(result)

    if defender is None:
        via.assertEqual(result, attacker)

    elif isinstance(defender, p.Flag):
        via.assertEqual(result, defender)

    elif (isinstance(defender, p.Bomb) and not
            isinstance(attacker, p.Miner)):
        via.assertEqual(result, defender)

    elif (isinstance(defender, p.Marshal) and
            isinstance(attacker, p.Spy)):
        via.assertEqual(result, attacker)

    elif isinstance(defender, p.Troop):
        if attacker.rank > defender.rank:
            via.assertEqual(result, attacker)

        elif attacker.rank == defender.rank:
            via.assertIsNone(result)

        else:
            via.assertEqual(result, defender)


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
        troop: p.Troop = p.Troop('BLUE', 9)

        with self.assertRaises(TypeError):
            bomb.confront(p.Troop)

        with self.assertRaises(TypeError):
            bomb.confront(p.Troop)

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

        for red_piece in red_pieces:
            if type(red_piece) not in {p.Troop, p.Scout}:
                continue

            for blue_piece in blue_pieces:
                red_rank = red_piece.rank
                blue_rank = blue_piece.rank

                if red_rank < blue_rank:
                    assert_confront(red_piece, blue_piece, blue_piece)
                    assert_confront(blue_piece, red_piece, blue_piece)

                elif red_rank > blue_rank:
                    assert_confront(red_piece, blue_piece, red_piece)
                    assert_confront(blue_piece, red_piece, red_piece)

                else:  # red_rank == blue_rank
                    assert_confront(red_piece, blue_piece, None)
                    assert_confront(blue_piece, red_piece, None)

    def test_spy_and_marshal(self) -> None:
        '''
        Tests the spy piece for stratego. The spy should defeat
        a marshal when the spy attacks, but not when the marshal
        attacks.
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
        # Create a flag and a regular troop
        flag: p.Flag = p.Flag('RED')
        troop: p.Troop = p.Troop('BLUE', 5)

        with self.assertRaises(TypeError):
            flag.confront(troop)

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
        miner: p.Miner = p.Miner('BLUE')
        bomb: p.Bomb = p.Bomb('RED')

        result: p.Piece = miner.confront(bomb)
        self.assertEqual(result, miner)

    def test_confrontation(self) -> None:
        '''
        Tests random confrontations between arbitrary pieces.
        '''

        # Options to permute over
        possible_colors: List[Literal['BLUE', 'RED']] = ['BLUE', 'RED']

        for color in possible_colors:
            other_color: Literal['BLUE', 'RED'] = \
                'RED' if color == 'BLUE' else 'BLUE'

            for attacker in all_pieces(color):

                if not isinstance(attacker, p.Troop):
                    continue

                for defender in all_pieces(other_color):
                    assert_confrontation_detailed(self, attacker, defender)

                assert_confrontation_detailed(self, attacker, None)
