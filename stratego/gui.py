'''
Defines a Stratego GUI. Should use OOP. Maybe inherit from
PyGame or Tkinter?

This class should aggregate the board and networking. This
is what should be presented to the user.
'''

import stratego.board
import stratego.pieces
import stratego.network


# To silence unused import warnings
help(stratego.board)
help(stratego.pieces)
help(stratego.network)


class StrategoGUI:
    '''
    An aggregate singleton class which encompasses the board,
    GUI, and networking of a Stratego game.
    '''
