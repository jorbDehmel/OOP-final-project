'''
Network operations for OOP Stratego. Should send the game state
from GUI to GUI via pickle. This could take the form of a
singleton API handler wrapper class.
'''

import pickle
import socket
import stratego.board


# To silence unused import warnings
help(stratego.board)
help(pickle)
help(socket)


class StrategoNetworker:
    '''
    Handles networking operations for Stratego. This is
    aggregated by the GUI class in stratego.gui.
    '''

    def __init__(self) -> None:
        '''
        Create infrastructure, but do NOT open socket yet.
        '''
