'''
Tests the `Board` class for OOP Stratego.
'''

import unittest
from stratego import board as b
from stratego import pieces as p


class TestBoard(unittest.TestCase):
    '''
    A test case for testing the stratego.board.Board class.
    '''

    def test_init(self) -> None:
        '''
        Tests __init__ and the singleton-ness of the Board
        class.
        '''

        board: b.Board = b.Board()

        with self.assertRaises(ValueError):
            b.Board()

        self.assertEqual(board.height, 10)
        self.assertEqual(board.width, 10)

        # Test populating
        board.set(0, 0, p.Troop('RED', 5))

        # Test repr
        repr(board)

        # Test getting

        # Test movement
