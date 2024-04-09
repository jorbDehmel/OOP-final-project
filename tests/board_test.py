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

        board: b.Board = b.Board.get_instance()

        with self.assertRaises(ValueError):
            b.Board()

        _ = b.Board.get_instance()

        self.assertEqual(board.height, 10)
        self.assertEqual(board.width, 10)

        # Test populating
        board.set_piece(0, 0, p.Troop('RED', 5))

        with self.assertRaises(ValueError):
            board.set_piece(-1, 0, board.get(0, 0))

        with self.assertRaises(ValueError):
            board.set_piece(0, 100, board.get(0, 0))

        # Test repr
        repr(board)

        # Test getting
        self.assertIsNone(board.get(-1, 0))
        self.assertIsNone(board.get(0, 11))

        result: b.Square = board.get(0, 0)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, p.Troop)
        self.assertEqual(result.color, 'RED')
        self.assertEqual(repr(result), '5')

        # Test movement
        board.set_piece(0, 1, p.Troop('BLUE', 4))
        board.move('RED', (0, 0), (0, 1))

        with self.assertRaises(b.InvalidMoveError):
            board.move('BLUE', (0, 1), (0, 0))

        with self.assertRaises(b.InvalidMoveError):
            board.move('RED', (0, 1), (0, 6))

        with self.assertRaises(b.InvalidMoveError):
            board.move('BLUE', (0, 1), (0, 15))

        with self.assertRaises(b.InvalidMoveError):
            board.move('BLUE', (0, 1), (0, 15))

        with self.assertRaises(b.InvalidMoveError):
            board.move('BLUE', (0, 1), (1, 2))

        with self.assertRaises(b.InvalidMoveError):
            board.move('BLUE', (0, 1), (0, 3))

        with self.assertRaises(b.InvalidMoveError):
            board.move('BLUE', (5, 5), (5, 6))
