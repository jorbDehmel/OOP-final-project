'''
Tests the `Board` class for OOP Stratego.
'''

from typing import Literal, List
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

    def test_all_pieces(self) -> None:
        '''
        Tests the `all_pieces` method, which returns all the
        pieces which need to be set up for a given color.
        '''

        for color in ['RED', 'BLUE']:
            expected: List[p.Piece] = ([p.Bomb(color)] * 6
                                    + [p.Scout(color)] * 8
                                    + [p.Miner(color)] * 5
                                    + [p.Marshal(color),
                                        p.Spy(color),
                                        p.Flag(color),
                                        p.Troop(color, 9),
                                        p.Troop(color, 8),
                                        p.Troop(color, 8)]
                                    + [p.Troop(color, 7)] * 3
                                    + [p.Troop(color, 6),
                                        p.Troop(color, 5),
                                        p.Troop(color, 4)] * 4)

            observed: List[p.Piece] = b.Board.all_pieces(color)

            for i, item in enumerate(expected):
                self.assertEqual(item.color, observed[i].color)
                self.assertEqual(repr(item), repr(observed[i]))

    def test_fill(self) -> None:
        '''
        Tests the b.Board.fill() function, which fills a given
        rectangular range with pieces according to either a
        given piece or a function.
        '''

        board: b.Board = b.Board.get_instance()
        board.clear()

        board.fill((0, 0), (10, 10), b.LakeSquare())

        for y in range(10):
            for x in range(10):
                self.assertIsInstance(board.get(x, y), b.LakeSquare)

        board.fill((0, 0), (10, 10), lambda x, y: b.LakeSquare()
                                                  if x < 5 else None)

        for y in range(10):
            for x in range(5):
                self.assertIsInstance(board.get(x, y), b.LakeSquare)
            for x in range(5, 10):
                self.assertIsNone(board.get(x, y))

    def test_moves(self) -> None:
        '''
        Tests various moves on the board.
        '''

        board: b.Board = b.Board.get_instance()
        board.clear()

        # Test populating
        board.set_piece(0, 0, p.Troop('RED', 5))

        with self.assertRaises(ValueError):
            board.set_piece(-1, 0, board.get(0, 0))

        with self.assertRaises(ValueError):
            board.set_piece(0, 100, board.get(0, 0))

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

        # Test move into empty space
        board.move('RED', (0, 1), (1, 1))

    def test_invalid_moves(self) -> None:
        '''
        Tests various invalid moves on the board.
        '''

        board: b.Board = b.Board.get_instance()
        board.clear()

        board.set_piece(0, 1, p.Troop('BLUE', 3))

        with self.assertRaises(b.InvalidMoveError):
            board.move('RED', (0, 1), (0, 6))

        with self.assertRaises(b.InvalidMoveError):
            board.move('RED', (0, 2), (0, 2))

        with self.assertRaises(b.InvalidMoveError):
            board.move('RED', (-1, 0), (0, 0))

        with self.assertRaises(b.InvalidMoveError):
            board.move('RED', (11, 0), (0, 0))

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

        # Assert that we cannot move a lake
        board.set_piece(0, 2, b.LakeSquare())
        self.assertIsInstance(board.get(0, 2), b.LakeSquare)
        with self.assertRaises(b.InvalidMoveError):
            board.move('BLUE', (0, 2), (0, 1))

        # We cannot move into lake
        with self.assertRaises(b.InvalidMoveError):
            board.move('BLUE', (0, 1), (0, 2))

    def test_colors(self):
        '''
        Ensures that you cannot move pieces which are not yours.
        '''

        board: b.Board = b.Board.get_instance()
        board.clear()

        board.set_piece(0, 0, p.Scout('BLUE'))
        board.set_piece(0, 9, p.Scout('RED'))

        with self.assertRaises(b.InvalidMoveError):
            board.move('RED', (0, 0), (0, 9))

        with self.assertRaises(b.InvalidMoveError):
            board.move('BLUE', (0, 9), (0, 0))

    def test_scout_movement(self) -> None:
        '''
        Tests the scout movement
        '''

        board: b.Board = b.Board.get_instance()
        board.clear()

        # Clear board
        for y in range(10):
            for x in range(10):
                board.set_piece(x, y, None)

        # Ensure non-scouts cannot move like them
        board.set_piece(0, 0, p.Troop('RED', 5))
        with self.assertRaises(b.InvalidMoveError):
            board.move('RED', (0, 0), (0, 9))
        with self.assertRaises(b.InvalidMoveError):
            board.move('RED', (0, 0), (9, 0))

        board.set_piece(0, 0, p.Scout('RED'))
        board.move('RED', (0, 0), (0, 9))
        board.move('RED', (0, 9), (0, 0))

        board.set_piece(0, 4, b.LakeSquare)
        board.set_piece(4, 0, b.LakeSquare)

        # Attempt to jump lakes
        with self.assertRaises(b.InvalidMoveError):
            board.move('RED', (0, 0), (0, 9))

        with self.assertRaises(b.InvalidMoveError):
            board.move('RED', (0, 0), (9, 0))

    def test_win_lose(self) -> None:
        '''
        Tests the win and lose conditions.
        '''

        board: b.Board = b.Board.get_instance()
        board.clear()

        board.set_piece(0, 0, p.Flag('RED'))
        board.set_piece(0, 1, p.Troop('BLUE', 6))

        state: Literal['RED', 'BLUE', 'GOOD'] = board.move('BLUE', (0, 1), (0, 0))

        # Assert that blue has won
        self.assertEqual(state, 'BLUE')

        board.set_piece(0, 1, p.Troop('RED', 6))

        # Ensure you cannot take your own flag
        with self.assertRaises(b.InvalidMoveError):
            board.move('RED', (0, 1), (0, 0))
