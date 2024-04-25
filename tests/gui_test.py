'''
Some tests of the Stratego GUI.
Jordan Dehmel, 2024
'''

from typing import Callable, Dict, List, Tuple
import unittest
from unittest import mock
import tkinter as tk
from hypothesis import given, strategies as some

import stratego.gui as g
import stratego.pieces as p
import stratego.board as b
import stratego.network as n


class GUITest(unittest.TestCase):
    '''
    Tests the Stratego GUI.
    '''

    class DummyNet:
        '''
        Dummy class
        '''

        def recv_game(self):
            '''
            Dummy function
            '''

            return (b.Board.get_instance(), 'GOOD')

        def send_game(self, _, __):
            '''
            Dummy function
            '''

        def host_game(self, _, port):
            '''
            Dummy function
            '''

            if port < 12350:
                raise OSError()

        def host_wait_for_join(self):
            '''
            Dummy function
            '''

        def close_game(self):
            '''
            Dummy function
            '''

        def join_game(self, _, __, ___):
            '''
            Dummy function
            '''

            return 0

    @classmethod
    def setUpClass(cls) -> None:
        '''
        Connects to the virtual X display.
        '''

        cls.root = tk.Tk(':99')

    def test_resize_image(self) -> None:
        '''
        Tests resizing images.
        '''

        # Connect to virtual display as set up externally
        tk.Tk()
        s: int = 16

        blank_img: tk.PhotoImage = tk.PhotoImage(file='stratego/images/blank.png')

        self.assertEqual(blank_img.width(), s)
        self.assertEqual(blank_img.height(), s)

        big_img: tk.PhotoImage = g.resize_image(blank_img, 128, 128)

        self.assertEqual(big_img.width(), 128)
        self.assertEqual(big_img.height(), 128)

        lake_img: tk.PhotoImage = tk.PhotoImage(file='stratego/images/lake.png')

        self.assertEqual(lake_img.width(), s)
        self.assertEqual(lake_img.height(), s)

        big_img = g.resize_image(lake_img, 128, 128)

        self.assertEqual(big_img.width(), 128)
        self.assertEqual(big_img.height(), 128)

    def test_color(self) -> None:
        '''
        Tests the color property.
        '''

        with mock.patch('tkinter.Tk'):

            g.StrategoGUI.clear_instance()
            gui: g.StrategoGUI = g.StrategoGUI.get_instance()

            gui.color = 'BLUE'
            self.assertEqual(gui.color, 'BLUE')

            gui.color = 'RED'
            self.assertEqual(gui.color, 'RED')

            gui.quit()

    @given(some.text())
    def test_gen_screens(self, text) -> None:
        '''
        Test the GUI screen setter via hypothesis testing.
        '''

        valid_cases: List[str] = ['HOME',
                                  'INFO',
                                  'WIN',
                                  'LOSE',
                                  'ERROR',
                                  'SETUP',
                                  'HOST_GAME',
                                  'JOIN_GAME',
                                  'YOUR_TURN',
                                  'THEIR_TURN']

        gui: g.StrategoGUI = g.StrategoGUI.get_instance()

        if text not in valid_cases:
            with self.assertRaises(AssertionError):
                gui.screen = text

    def test_misc_screens(self) -> None:
        '''
        Test the GUI's screens via patching.
        '''

        with mock.patch('tkinter.Tk') as fake_tk:

            # Setup winfo_children
            fake_tk.winfo_children.return_value = [mock.Mock()] * 5

            # This has no public methods other than get_instance
            g.StrategoGUI.clear_instance()
            gui: g.StrategoGUI = g.StrategoGUI.get_instance()

            gui.screen = 'HOME'
            gui.screen = 'INFO'
            gui.screen = 'ERROR'
            gui.screen = 'WIN'
            gui.screen = 'LOSE'

            gui.quit()

    def test_win(self) -> None:
        '''
        Tests making a move via the GUI. This should result in
        a win screen.
        '''

        for color in ['RED', 'BLUE']:

            with (mock.patch('tkinter.Tk'),
                  mock.patch.object(n, 'StrategoNetworker', GUITest.DummyNet),
                  mock.patch('tkinter.Button') as fake_button):

                other_color: str = 'RED' if color == 'BLUE' else 'BLUE'

                g.StrategoGUI.clear_instance()
                b.Board.get_instance().clear()
                gui: g.StrategoGUI = g.StrategoGUI.get_instance()
                gui.color = color

                gui.board.set_piece(0, 9, p.Scout(color))
                gui.board.set_piece(9, 9, p.Flag(other_color))

                gui.screen = 'YOUR_TURN'

                # Capture buttons
                buttons: List[Callable[[], None]] = []

                # Iterate over patched constructor calls
                for item in fake_button.mock_calls:
                    kwargs = item[2]  # Get only kwargs from mock call

                    # Skip if not a commanded textless button
                    if 'command' not in kwargs or 'text' in kwargs:
                        continue

                    # Add to dictionary
                    buttons.append(kwargs['command'])

                self.assertIsInstance(gui.board.get(0, 9), p.Scout)
                self.assertIsInstance(gui.board.get(9, 9), p.Flag)

                # Simulate press on (0, 9) (scout)
                did_press: bool = False
                for item in buttons:
                    if item.x == 0 and item.y == 9:
                        item()
                        did_press = True
                        break

                assert did_press

                # Simulate press on (9, 9) (opponent's flag)
                did_press = False
                for item in buttons:
                    if item.x == 9 and item.y == 9:
                        item()
                        did_press = True
                        break

                assert did_press

                self.assertIsNone(gui.board.get(0, 9))
                self.assertIsInstance(gui.board.get(9, 9), p.Flag)

                self.assertEqual(gui.screen, 'WIN')

    def test_lose(self) -> None:
        '''
        Tests receiving a losing move via the GUI. This should
        result in a loss.
        '''

        for color in ['RED', 'BLUE']:

            other_color: str = 'RED' if color == 'BLUE' else 'BLUE'

            def dummy_network_replacement(_) -> Tuple[b.Board, str]:
                nonlocal other_color
                return (b.Board.get_instance(), other_color)

            with (mock.patch('tkinter.Tk') as fake_tk,
                  mock.patch.object(n.StrategoNetworker, 'recv_game',
                                    dummy_network_replacement)):

                # Setup winfo_children
                fake_tk.winfo_children.return_value = [mock.Mock()] * 5

                # Setup GUI
                g.StrategoGUI.clear_instance()
                gui: g.StrategoGUI = g.StrategoGUI.get_instance()
                gui.color = color

                gui.screen = 'THEIR_TURN'

                # This will call the patched networker
                # The networker will send a dummy board and a
                # signal that we have lost the game. This should
                # cause the GUI to transition to the loss
                # screen.

                self.assertEqual(gui.screen, 'LOSE')

    def test_error_1(self) -> None:
        '''
        Tests receiving an error via the GUI. This should
        result in an error screen.
        '''

        for color in ['RED', 'BLUE']:

            def dummy_network_replacement(self,
                                          _: b.Board,
                                          __: str) -> None:
                raise ValueError('This was raised by a dummy')

            with (mock.patch('tkinter.Tk'),
                  mock.patch.object(n.StrategoNetworker, 'send_game',
                                    dummy_network_replacement),
                  mock.patch('tkinter.Button') as fake_button):

                other_color: str = 'RED' if color == 'BLUE' else 'BLUE'

                g.StrategoGUI.clear_instance()
                b.Board.get_instance().clear()
                gui: g.StrategoGUI = g.StrategoGUI.get_instance()
                gui.color = color

                gui.board.set_piece(0, 9, p.Scout(color))
                gui.board.set_piece(9, 9, p.Flag(other_color))

                gui.screen = 'YOUR_TURN'

                # Capture buttons
                buttons: List[Callable[[], None]] = []

                # Iterate over patched constructor calls
                for item in fake_button.mock_calls:
                    kwargs = item[2]  # Get only kwargs from mock call

                    # Skip if not a commanded textless button
                    if 'command' not in kwargs or 'text' in kwargs:
                        continue

                    # Add to dictionary
                    buttons.append(kwargs['command'])

                self.assertIsInstance(gui.board.get(0, 9), p.Scout)
                self.assertIsInstance(gui.board.get(9, 9), p.Flag)

                # Simulate press on (0, 9) (scout)
                for item in buttons:
                    if item.x == 0 and item.y == 9:
                        item()
                        break

                # Simulate press on (9, 9) (opponent's flag)
                for item in buttons:
                    if item.x == 9 and item.y == 9:
                        item()
                        break

                # Here, it should try to send the game, which
                # will cause an error.

                self.assertEqual(gui.screen, 'ERROR')

    def test_error_2(self) -> None:
        '''
        Tests receiving an error via the GUI. This should
        result in an error screen.
        '''

        def dummy_network_replacement(self) -> None:
            raise ValueError('This was raised by a dummy')

        with (mock.patch('tkinter.Tk'),
              mock.patch.object(n.StrategoNetworker, 'recv_game',
                                dummy_network_replacement),
              mock.patch.object(n.StrategoNetworker, 'send_game'),
              mock.patch('tkinter.Button') as fake_button):

            g.StrategoGUI.clear_instance()
            b.Board.get_instance().clear()
            gui: g.StrategoGUI = g.StrategoGUI.get_instance()

            color: str = 'RED'
            other_color: str = 'BLUE'

            gui.color = color

            gui.board.set_piece(0, 9, p.Scout(color))
            gui.board.set_piece(9, 9, p.Flag(other_color))

            gui.screen = 'YOUR_TURN'

            # Capture buttons
            buttons: List[Callable[[], None]] = []

            # Iterate over patched constructor calls
            for item in fake_button.mock_calls:
                kwargs = item[2]  # Get only kwargs from mock call

                # Skip if not a commanded textless button
                if 'command' not in kwargs or 'text' in kwargs:
                    continue

                # Add to dictionary
                buttons.append(kwargs['command'])

            self.assertIsInstance(gui.board.get(0, 9), p.Scout)
            self.assertIsInstance(gui.board.get(9, 9), p.Flag)

            # Simulate press on (0, 9) (scout)
            for item in buttons:
                if item.x == 0 and item.y == 9:
                    item()
                    break

            # Simulate press on (5, 9)
            for item in buttons:
                if item.x == 5 and item.y == 9:
                    item()
                    break

            # Here, it should send the game successfully via
            # mock. Then, it will expect a recv-ed game, which
            # will error.
            self.assertEqual(gui.screen, 'ERROR')

    def test_error_3(self) -> None:
        '''
        Tests receiving an error via the GUI. This should
        result in an error screen.
        '''

        with (mock.patch('tkinter.Tk'),
              mock.patch.object(n, 'StrategoNetworker'),
              mock.patch('tkinter.Button') as fake_button):

            g.StrategoGUI.clear_instance()
            b.Board.get_instance().clear()
            gui: g.StrategoGUI = g.StrategoGUI.get_instance()

            color: str = 'RED'
            other_color: str = 'BLUE'

            gui.color = color

            gui.board.set_piece(0, 9, p.Scout(color))
            gui.board.set_piece(9, 9, p.Flag(other_color))

            gui.screen = 'YOUR_TURN'

            # Capture buttons
            buttons: List[Callable[[], None]] = []

            # Iterate over patched constructor calls
            for item in fake_button.mock_calls:
                kwargs = item[2]  # Get only kwargs from mock call

                # Skip if not a commanded textless button
                if 'command' not in kwargs or 'text' in kwargs:
                    continue

                # Add to dictionary
                buttons.append(kwargs['command'])

            self.assertIsInstance(gui.board.get(0, 9), p.Scout)

            # Simulate press on (0, 9) (scout)
            for item in buttons:
                if item.x == 0 and item.y == 9:
                    item()
                    break

            # Simulate press on (5, 5)
            for item in buttons:
                if item.x == 5 and item.y == 5:
                    item()
                    break

            # Here, it will detect an invalid move, causing it
            # to remain on this screen.

            self.assertEqual(gui.screen, 'YOUR_TURN')

    def test_host(self) -> None:
        '''
        Test the GUI's hosting screen via patching.
        '''

        with (mock.patch('tkinter.Tk'),
              mock.patch.object(n, 'StrategoNetworker', GUITest.DummyNet)):

            # This has no public methods other than get_instance
            g.StrategoGUI.clear_instance()
            gui: g.StrategoGUI = g.StrategoGUI.get_instance()

            # Get to host screen
            gui.screen = 'HOST_GAME'
            gui.press_key('<Return>')

            gui.quit()

    def test_join(self) -> None:
        '''
        Test the GUI's joining screen via patching.
        '''

        with (mock.patch('tkinter.Tk'),
              mock.patch.object(n, 'StrategoNetworker', GUITest.DummyNet)):

            # This has no public methods other than get_instance
            g.StrategoGUI.clear_instance()
            gui: g.StrategoGUI = g.StrategoGUI.get_instance()

            # Get to host screen
            gui.screen = 'JOIN_GAME'
            gui.press_key('<Return>')

            gui.quit()

    def test_join_2(self) -> None:
        '''
        Test the GUI's joining screen via patching.
        '''

        with (mock.patch('tkinter.Tk'),
              mock.patch('tkinter.Entry') as fake_entry,
              mock.patch.object(n, 'StrategoNetworker', GUITest.DummyNet)):

            fake_entry.get.return_value = ''

            # This has no public methods other than get_instance
            g.StrategoGUI.clear_instance()
            gui: g.StrategoGUI = g.StrategoGUI.get_instance()

            # Get to host screen
            gui.screen = 'JOIN_GAME'
            gui.press_key('<Return>')

            gui.quit()

    def test_setup_1(self) -> None:
        '''
        Test the GUI's setup screen via patching.
        '''

        n.StrategoNetworker.clear_instance()
        g.StrategoGUI.clear_instance()
        b.Board.clear_instance()

        for color in ['RED', 'BLUE']:
            with (mock.patch('tkinter.Tk'),
                  mock.patch('tkinter.Button') as fake_button,
                  mock.patch.object(n, 'StrategoNetworker', GUITest.DummyNet)):

                g.StrategoGUI.clear_instance()
                b.Board.clear_instance()

                g.StrategoGUI.clear_instance()
                gui: g.StrategoGUI = g.StrategoGUI.get_instance()

                # Initialize host game interface
                gui.screen = 'HOST_GAME'
                self.assertEqual(gui.screen, 'HOST_GAME')

                # Simulate pressing enter, moving on to next screen
                # This will call host_game, then wait for join game
                gui.press_key('<Return>')
                gui.color = color

                # Here, the networking object attempts to connect
                # with the patched socket. If successful, it will
                # move on to the setup screen.

                self.assertEqual(gui.screen, 'SETUP')

                # Unwrap all labeled buttons currently on screen
                buttons: Dict[str, Callable[[], None]] = {}

                # Iterate over patched constructor calls
                for item in fake_button.mock_calls:
                    kwargs = item[2]  # Get only kwargs from mock call

                    # Skip if not a labeled button
                    if 'command' not in kwargs or 'text' not in kwargs:
                        continue

                    # Add to dictionary
                    buttons[kwargs['text']] = kwargs['command']

                # Call the randomize all function via the fetched
                # buttons
                self.assertIn('Randomize all', buttons)
                buttons['Randomize all']()

                gui.screen = 'THEIR_TURN'
                gui.screen = 'YOUR_TURN'

            gui.quit()

    def test_setup_2(self) -> None:
        '''
        Test the GUI's setup screen via patching.
        '''

        n.StrategoNetworker.clear_instance()
        g.StrategoGUI.clear_instance()
        b.Board.clear_instance()

        for color in ['RED', 'BLUE']:

            with (mock.patch('tkinter.Button') as fake_button,
                  mock.patch.object(n, 'StrategoNetworker', GUITest.DummyNet),
                  mock.patch('tkinter.Tk')):

                g.StrategoGUI.clear_instance()
                b.Board.clear_instance()

                gui: g.StrategoGUI = g.StrategoGUI.get_instance()

                # Initialize host game interface
                gui.screen = 'HOST_GAME'
                self.assertEqual(gui.screen, 'HOST_GAME')

                # Simulate pressing enter, moving on to next screen
                # This will call host_game, then wait for join game
                gui.press_key('<Return>')
                gui.color = color

                # Here, the networking object attempts to connect
                # with the patched socket. If successful, it will
                # move on to the setup screen.

                button_dict: Dict[Tuple[int, int], Callable[[], None]] = {}
                for item in [item[2]['command'] for item in fake_button.mock_calls
                             if 'command' in item[2] and 'text' not in item[2]]:
                    button_dict[(item.x, item.y)] = item

                # These two calls will validate both colors. One
                # will be valid, and the other will be invalid.

                # Simulate two presses on (0, 0)
                button_dict[(0, 0)]()
                button_dict[(0, 0)]()

                # Simulate two presses on (9, 9)
                button_dict[(9, 9)]()
                button_dict[(9, 9)]()

            gui.quit()

    def test_setup_3(self) -> None:
        '''
        Test the GUI's setup screen via patching.
        '''

        for color in ['RED', 'BLUE']:

            with (mock.patch('tkinter.Tk'),
                  mock.patch('tkinter.Button') as fake_button,
                  mock.patch.object(n, 'StrategoNetworker', GUITest.DummyNet)):

                gui: g.StrategoGUI = g.StrategoGUI.get_instance()

                gui.screen = 'HOST_GAME'
                gui.press_key('<Return>')
                gui.color = color

                button_dict: Dict[Tuple[int, int], Callable[[], None]] = {}
                for item in [item[2]['command'] for item in fake_button.mock_calls
                             if 'command' in item[2] and 'text' not in item[2]]:
                    button_dict[(item.x, item.y)] = item

                # Now we test what would happen if we placed
                # every piece manually.

                for x in range(10):
                    if color == 'RED':
                        for y in range(0, 4):
                            button_dict[(x, y)]()

                    # Blue is able to place pieces in the BOTTOM 4 rows
                    else:
                        for y in range(6, 10):
                            button_dict[(x, y)]()
