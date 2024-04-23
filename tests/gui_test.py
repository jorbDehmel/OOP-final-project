'''
Some tests of the Stratego GUI.
Jordan Dehmel, 2024
'''

from typing import Callable, Dict, List, Tuple
import unittest
from unittest import mock
import tkinter as tk
import stratego.gui as g
import stratego.pieces as p
import stratego.board as b
import stratego.network as n


class GUITest(unittest.TestCase):
    '''
    Tests the Stratego GUI.
    '''

    class TKDummy:
        '''
        A special class to replace tkinter._default_root
        with in order to avoid errors. The methods defined
        herein are required in order for this to run without
        error.
        '''

        def call(self, args=None, kwargs=None) -> None:
            '''
            Dummy function.
            '''

        def getint(self, args=None, kwargs=None) -> None:
            '''
            Dummy function.
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

        def host_game(self, _, __):
            '''
            Dummy function
            '''

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

    def test_resize_image(self) -> None:
        '''
        Tests resizing images.
        '''

        tk.Tk()

        blank_img: tk.PhotoImage = tk.PhotoImage('stratego/images/blank.png')

        big_img: tk.PhotoImage = g.resize_image(blank_img, 1024, 1024)

        self.assertEqual(big_img.width(), 1024)
        self.assertEqual(big_img.height(), 1024)

        lake_img: tk.PhotoImage = tk.PhotoImage('stratego/images/lake.png')

        big_img = g.resize_image(lake_img, 1024, 1024)

        self.assertEqual(big_img.width(), 1024)
        self.assertEqual(big_img.height(), 1024)

    def test_color(self) -> None:
        '''
        Tests the color property.
        '''

        with mock.patch('tkinter.Tk'):

            # This has no public methods other than get_instance
            gui: g.StrategoGUI = g.StrategoGUI.get_instance()

            gui.color = 'BLUE'
            self.assertEqual(gui.color, 'BLUE')

            gui.color = 'RED'
            self.assertEqual(gui.color, 'RED')

            gui.quit()

    def test_misc_screens(self) -> None:
        '''
        Test the GUI's screens via patching.
        '''

        with (mock.patch('tkinter.Tk') as fake_tk,
              mock.patch('tkinter._default_root', GUITest.TKDummy)):

            # Setup winfo_children
            fake_tk.winfo_children.return_value = [mock.Mock()] * 5

            # This has no public methods other than get_instance
            gui: g.StrategoGUI = g.StrategoGUI.get_instance()

            gui.screen = 'HOME'
            self.assertEqual(gui.screen, 'HOME')  # Tests setter

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
                  mock.patch('tkinter._default_root', GUITest.TKDummy),
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
                for item in buttons:
                    if item.x == 0 and item.y == 9:
                        item()
                        break

                # Simulate press on (9, 9) (opponent's flag)
                for item in buttons:
                    if item.x == 9 and item.y == 9:
                        item()
                        break

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

            g.StrategoGUI.clear_instance()

            with (mock.patch('tkinter.Tk'),
                  mock.patch('tkinter._default_root', GUITest.TKDummy),
                  mock.patch.object(n.StrategoNetworker, 'recv_game',
                                    dummy_network_replacement)):

                # Setup GUI
                gui: g.StrategoGUI = g.StrategoGUI.get_instance()
                gui.color = color

                gui.screen = 'THEIR_TURN'

                # This will call the patched networker
                # The networker will send a dummy board and a
                # signal that we have lost the game. This should
                # cause the GUI to transition to the loss
                # screen.

                self.assertEqual(gui.screen, 'LOSE')

    def test_error(self) -> None:
        '''
        Tests receiving a losing move via the GUI. This should
        result in a loss.
        '''

        for color in ['RED', 'BLUE']:

            def dummy_network_replacement(self,
                                          _: b.Board,
                                          __: str) -> None:
                raise ValueError('This was raised by a dummy')

            with (mock.patch('tkinter.Tk'),
                  mock.patch('tkinter._default_root', GUITest.TKDummy),
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

    def test_host(self) -> None:
        '''
        Test the GUI's hosting screen via patching.
        '''

        with (mock.patch('tkinter.Tk'),
              mock.patch('tkinter._default_root', GUITest.TKDummy),
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
              mock.patch('tkinter._default_root', GUITest.TKDummy),
              mock.patch.object(n, 'StrategoNetworker', GUITest.DummyNet)):

            # This has no public methods other than get_instance
            gui: g.StrategoGUI = g.StrategoGUI.get_instance()

            # Get to host screen
            gui.screen = 'JOIN_GAME'
            gui.press_key('<Return>')

            gui.quit()

    def test_setup(self) -> None:
        '''
        Test the GUI's setup screen via patching.
        '''

        n.StrategoNetworker.clear_instance()
        g.StrategoGUI.clear_instance()
        b.Board.clear_instance()

        with (mock.patch('tkinter.Tk'),
              mock.patch('tkinter.Button') as fake_button,
              mock.patch.object(n, 'StrategoNetworker', GUITest.DummyNet),
              mock.patch('tkinter._default_root', GUITest.TKDummy)):

            for color in ['RED', 'BLUE']:

                g.StrategoGUI.clear_instance()
                b.Board.clear_instance()

                g.StrategoGUI.clear_instance()
                gui: g.StrategoGUI = g.StrategoGUI.get_instance()

                # Initialize host game interface
                gui.color = color
                gui.screen = 'HOST_GAME'

                # Simulate pressing enter, moving on to next screen
                # This will call host_game, then wait for join game
                gui.press_key('<Return>')

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
