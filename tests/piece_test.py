'''
Tests the `Piece` classes for OOP Stratego.
'''

from typing import Optional, List, TypeAlias
from unittest import TestCase
from stratego import pieces as p
from stratego import board as b


class TestStrategoPiece(TestCase):
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
        bomb: p.Bomb = p.Bomb('RED')
        troop: p.Troop = p.Troop('BLUE', 5)

        with self.assertRaises(TypeError):
            bomb.confront(troop)

        self.assertEqual(repr(bomb), 'B')
        self.assertEqual(repr(troop), '5')

        # Simulate an interaction between the two
        result: Optional[p.Piece] = troop.confront(bomb)
        assert result is bomb

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

        # Create a flag and a regular troop
        flag: p.Flag = p.Flag('RED')
        troop: p.Troop = p.Troop('BLUE', 5)

        with self.assertRaises(TypeError):
            flag.confront(troop)

    def test_spy_and_marshal(self) -> None:
        '''
        Tests the spy piece for stratego. The spy should defeat
        a marshal when the spy attacks, but not when the marshal
        attacks.
        '''

        s: p.Spy = p.Spy('RED')
        m: p.Marshal = p.Marshal('BLUE')

        self.assertEqual(s.confront(m), s)
        self.assertEqual(m.confront(s), m)

    def test_miner(self) -> None:
        '''
        Tests the miner piece for stratego. The miner is able to
        defuse bombs.
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
        possible_types: List[TypeAlias] = [None, b.LakeSquare,
                                           p.Bomb, p.Flag, p.Marshal,
                                           p.Miner, p.Scout, p.Spy]
        possible_colors: List[str] = ['BLUE', 'RED']
        possible_troop_ranks: List[int] = [4, 5, 6, 7, 8, 9]

        all_pieces: List[b.Square] = []

        for color in possible_colors:

            for possible_type in possible_types:
                if possible_type is None:
                    all_pieces.append(None)

                elif possible_type is b.LakeSquare:
                    all_pieces.append(b.LakeSquare())

                else:
                    all_pieces.append(possible_type(color))

                    self.assertEqual(all_pieces[-1].color, color)

            for rank in possible_troop_ranks:
                all_pieces.append(p.Troop(color, rank))

        for attacker in all_pieces:

            if not isinstance(attacker, p.Troop):
                continue

            for defender in all_pieces:
                if defender is attacker:
                    continue

                result: Optional[p.Piece] = attacker.confront(defender)

                repr(attacker)
                repr(defender)
                repr(result)

                if defender is None:
                    self.assertEqual(result, attacker)

                elif isinstance(defender, p.Flag):
                    self.assertEqual(result, defender)

                elif (isinstance(defender, p.Bomb) and not
                      isinstance(attacker, p.Miner)):
                    self.assertEqual(result, defender)

                elif (isinstance(defender, p.Marshal) and
                      isinstance(attacker, p.Spy)):
                    self.assertEqual(result, attacker)

                elif isinstance(defender, p.Troop):
                    if attacker.rank > defender.rank:
                        self.assertEqual(result, attacker)

                    elif attacker.rank == defender.rank:
                        self.assertIsNone(result)

                    else:
                        self.assertEqual(result, defender)
