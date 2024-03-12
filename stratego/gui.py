'''
Defines a Stratego GUI. Should use OOP. Maybe inherit from
PyGame or use Tkinter.

This class should aggregate the board and networking. This
is what should be presented to the user.
'''

from typing import Optional
import stratego.board as b
import stratego.network as n


class StrategoGUI:
    '''
    An aggregate singleton class which encompasses the board,
    GUI, and networking of a Stratego game.
    '''

    __INSTANCE: Optional['StrategoGUI'] = None

    @classmethod
    def get_instance(cls) -> 'StrategoGUI':
        '''
        Returns the instance of this class, instantiating if
        none already exist.

        :returns: The instance of this singleton class.
        '''

        if cls.__INSTANCE is None:
            cls.__INSTANCE = StrategoGUI()

        return cls.__INSTANCE

    def __init__(self) -> None:
        '''
        Initialize the GUI window, given that none already
        exists.
        '''

        assert type(self).__INSTANCE is None, 'Cannot reinstantiate singleton'

        self.__board: b.Board = b.Board()
        self.__networking: n.StrategoNetworker = n.StrategoNetworker()

        self.__start_gui()

    # button callbacks here

    def __start_gui(self) -> None:
        '''
        The host/connect screen of the app.
        '''

    # GUI setup functions here
