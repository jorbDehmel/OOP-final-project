'''
Some tests of the Stratego GUI.
'''

from typing import Callable, Dict
import unittest
from unittest import mock
import tkinter as tk

import stratego
import stratego.gui
import stratego.network


class HelperTest(unittest.TestCase):
    '''
    Tests helper function(s).
    '''

    def test_resize_image(self) -> None:
        '''
        Tests resize_image.
        '''

        # Initialize TK; This theoretically avoids errors
        tk.Tk()

        empty: tk.PhotoImage = tk.PhotoImage()

        big_empty = stratego.gui.resize_image(empty, 1024, 1024)
        self.assertEqual(big_empty.width(), 1024)
        self.assertEqual(big_empty.height(), 1024)


class GUITest(unittest.TestCase):
    '''
    Tests the Stratego GUI.
    '''

    def test_color(self) -> None:
        '''
        Tests the color property.
        '''

        with mock.patch('tkinter.Tk') as _:

            # This has no public methods other than get_instance
            gui: stratego.gui.StrategoGUI = stratego.gui.StrategoGUI.get_instance()

            gui.color = 'BLUE'
            self.assertEqual(gui.color, 'BLUE')

            gui.color = 'RED'
            self.assertEqual(gui.color, 'RED')

            gui.quit()

    def test_misc_screens(self) -> None:
        '''
        Test the GUI's screens via patching.
        '''

        with mock.patch('tkinter.Tk') as fake_tk:

            # Setup winfo_children
            fake_tk.winfo_children.return_value = [mock.Mock()] * 5

            # This has no public methods other than get_instance
            gui: stratego.gui.StrategoGUI = stratego.gui.StrategoGUI.get_instance()

            gui.screen = 'HOME'
            self.assertEqual(gui.screen, 'HOME')  # Tests setter

            gui.screen = 'INFO'
            gui.screen = 'ERROR'
            gui.screen = 'WIN'
            gui.screen = 'LOSE'

            gui.quit()

    def test_host(self) -> None:
        '''
        Test the GUI's hosting screen via patching.
        '''

        with mock.patch('tkinter.Tk') as _:

            # This has no public methods other than get_instance
            gui: stratego.gui.StrategoGUI = stratego.gui.StrategoGUI.get_instance()

            # Get to host screen
            gui.screen = 'HOST_GAME'

            gui.quit()

    def test_join(self) -> None:
        '''
        Test the GUI's joining screen via patching.
        '''

        with mock.patch('tkinter.Tk') as _:

            # This has no public methods other than get_instance
            gui: stratego.gui.StrategoGUI = stratego.gui.StrategoGUI.get_instance()

            # Get to host screen
            gui.screen = 'JOIN_GAME'

            gui.quit()

    def test_setup(self) -> None:
        '''
        Test the GUI's setup screen via patching.
        '''

        with (mock.patch('tkinter.Tk') as _,
              mock.patch('tkinter.Button') as fake_button,
              mock.patch('stratego.network.StrategoNetworker') as fake_net):

            fake_net.recv_game.return_value = (stratego.board.Board.get_instance(), 'GOOD')

            stratego.gui.StrategoGUI.clear_instance()
            gui: stratego.gui.StrategoGUI = stratego.gui.StrategoGUI.get_instance()

            # Initialize host game interface
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
