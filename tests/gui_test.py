'''
Some tests of the Stratego GUI.
'''

import unittest
from unittest import mock
from stratego import gui as g


class GUITest(unittest.TestCase):
    '''
    Tests the Stratego GUI.
    '''

    def test_init(self) -> None:
        '''
        Test g.StrategoGUI.__init__() via patching.
        '''

        with mock.patch('tkinter.Tk'):
            g.StrategoGUI()
