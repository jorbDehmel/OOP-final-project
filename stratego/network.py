'''
Network operations for OOP Stratego. Should send the game state
from GUI to GUI via pickle. This could take the form of a
singleton API handler wrapper class.
'''

import pickle
import socket
import stratego.board
import stratego.pieces
