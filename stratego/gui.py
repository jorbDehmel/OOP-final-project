'''
Defines a Stratego GUI using tkinter. This class should
aggregate the board and networking. This is what should be
presented to the user.
'''

import tkinter as tk
from typing import Optional, List
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

        self.__root: tk.Tk = tk.Tk()

        self.__board: b.Board = b.Board()
        self.__networking: n.StrategoNetworker = n.StrategoNetworker()
        self.__color: str = 'N/A'

        self.__keybindings: List[str] = []

        # This keybinding is not tracked and thus not erased
        self.__root.bind('q', lambda _: self.__quit())

        self.__home_screen()

    def __home_screen(self) -> None:
        '''
        The host/connect screen of the app.
        '''

        tk.Label(self.__root, text='Stratego').pack()

        tk.Button(self.__root, text='Host Game', command=self.__host_game_screen).pack()
        tk.Button(self.__root, text='Join Game', command=self.__join_game_screen).pack()

        tk.Button(self.__root, text='Quit', command=self.__quit).pack()

        self.__bind('h', self.__host_game_screen)
        self.__bind('j', self.__join_game_screen)

        self.__root.mainloop()

    def __bind(self, sequence: str, event: callable) -> None:
        '''
        Bind the given sequence to the given callable. The
        callable will be passed no arguments. Any keybinding
        registered in this way will be erased by the clear()
        method.
        '''

        self.__root.bind(sequence, lambda _: event())
        self.__keybindings.append(sequence)

    def __quit(self) -> None:
        '''
        Button callback function for quitting the app.
        '''

        self.__root.destroy()

    def __clear(self) -> None:
        '''
        Destroy all children and free all registered
        keybindings.
        '''

        # Destroy all children
        for child in self.__root.winfo_children():
            child.destroy() # Metal

        # Unbind all keybindings registered herein
        for key in self.__keybindings:
            self.__root.unbind(key)

    def __host_game_screen(self) -> None:
        '''
        The screen which allows you to initiate hosting a game.
        '''

        # Clear screen
        self.__clear()

        # Build form fields
        tk.Label(self.__root, text='IP:').pack()
        ip: tk.Entry = tk.Entry(self.__root)
        ip.pack()

        tk.Label(self.__root, text='Port:').pack()
        port: tk.Entry = tk.Entry(self.__root)
        port.pack()

        def host_game_callback() -> None:
            '''
            Host a game
            '''

            # Extract fields
            ip_str: str = ip.get()
            port_int: int = int(port.get())

            password: str = self.__networking.host_game(ip_str, port_int)

            # Display waiting text
            self.__clear()
            tk.Label(self.__root,
                     text=f'IP: {ip_str} Port: {port_int}'
                          + f'Password: {password}').pack()
            tk.Label(self.__root,
                     text='Waiting for other player...').pack()

            # Make API call and wait
            self.__networking.host_wait_for_join()

            # When API call is done, advance to next screen
            self.__color = 'RED'
            self.__setup_screen()

        tk.Button(self.__root,
                  text='Host This Game',
                  command=host_game_callback).pack()

    def __join_game_screen(self) -> None:
        '''
        The screen which allows you to join an existing game.
        '''

        # Clear screen
        self.__clear()

        # Build form fields
        tk.Label(self.__root, text='IP:').pack()
        ip: tk.Entry = tk.Entry(self.__root)
        ip.pack()

        tk.Label(self.__root, text='Port:').pack()
        port: tk.Entry = tk.Entry(self.__root)
        port.pack()

        tk.Label(self.__root, text='Password:').pack()
        password: tk.Entry = tk.Entry(self.__root)
        password.pack()

        def join_game_callback() -> None:
            '''
            Join a game
            '''

            # Extract fields
            ip_str: str = ip.get()
            port_int: int = int(port.get())
            password_str: str = password.get()

            # Make API call and wait
            self.__networking.join_game(ip_str, port_int, password_str)

            # When API call is done, advance to next screen
            self.__color = 'BLUE'
            self.__setup_screen()

        tk.Button(self.__root,
                  text='Join This Game',
                  command=join_game_callback).pack()

    def __setup_screen(self) -> None:
        '''
        The board setup screen.
        '''

    def __your_turn_screen(self) -> None:
        '''
        Screen allowing our player to make a move.
        '''

    def __their_turn_screen(self) -> None:
        '''
        Waiting screen while the other player moves.
        '''

    def __win_screen(self) -> None:
        '''
        Shown when our player wins.
        '''

        self.__clear()

        self.__networking.close_game()

        tk.Label(self.__root, text='You win!').pack()

        tk.Button(self.__root,
                  text='Play Again',
                  command=self.__home_screen).pack()
        tk.Button(self.__root,
                  text='Quit',
                  command=self.__quit).pack()

    def __lose_screen(self) -> None:
        '''
        Shown when our player loses.
        '''

        self.__clear()

        self.__networking.close_game()

        tk.Label(self.__root, text='You lose...').pack()

        tk.Button(self.__root,
                  text='Play Again',
                  command=self.__home_screen).pack()
        tk.Button(self.__root,
                  text='Quit',
                  command=self.__quit).pack()

    def __error_screen(self) -> None:
        '''
        Shown when an error occurs (IE when the other user drops
        out unexpectedly).
        '''

        self.__clear()

        self.__networking.close_game()

        tk.Label(self.__root, text='Erro: Connection terminated.').pack()

        tk.Button(self.__root,
                  text='Play Again',
                  command=self.__home_screen).pack()
        tk.Button(self.__root,
                  text='Quit',
                  command=self.__quit).pack()
