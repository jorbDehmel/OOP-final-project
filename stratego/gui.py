'''
Defines a Stratego GUI using tkinter. This class should
aggregate the board and networking. This is what should be
presented to the user.
'''

import tkinter as tk
from typing import Optional, List, Callable, Tuple, Dict
from PIL import Image, ImageTk
import stratego.board as b
import stratego.network as n
import stratego.pieces as p


class StrategoGUI:
    '''
    An aggregate singleton class which encompasses the board,
    GUI, and networking of a Stratego game.
    '''

    __INSTANCE: Optional['StrategoGUI'] = None
    _BUTTON_SIZE: int = 32

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
        exist.
        '''

        assert type(self).__INSTANCE is None, 'Cannot reinstantiate singleton'

        self.__root: tk.Tk = tk.Tk()

        self.__root.option_add('*Font', 'Times 16')
        self.__root.geometry("384x416")

        self.__board: b.Board = b.Board()
        self.__networking: n.StrategoNetworker = n.StrategoNetworker()
        self.__color: str = 'Stratego'

        self.__keybindings: List[str] = []
        self.__image_cache: Dict[str, tk.PhotoImage] = {}

        self.__from_selection: Optional[Tuple[int, int]] = None
        self.__to_selection: Optional[Tuple[int, int]] = None

        self.__left_to_place: List[p.Piece] = []

        # This keybinding is not tracked and thus not erased
        self.__root.bind('q', lambda _: self.__quit())

        self.__root.title(self.__color)
        self.__home_screen()

    def __piece_to_image_path(self, piece: b.Square) -> str:
        '''
        Given a piece, returns the filepath of the image which
        should represent it.

        :param piece: The square to represent.
        :return: The filepath of the image.
        '''

        if piece is not None:

            if isinstance(piece, b.LakeSquare):
                return 'stratego/images/lake.png'

            if isinstance(piece, p.Piece):

                if piece.color != self.__color:
                    return f'stratego/images/{piece.color}_blank.png'

                return f'stratego/images/{piece.color}_{repr(piece)}.png'

        return 'stratego/images/blank.png'

    def __get_image(self, path: str) -> tk.PhotoImage:
        '''
        :param path: The path to load the image from.
        :returns: A tk-compatible version of that image.
        '''

        if path not in self.__image_cache:
            s: int = type(self)._BUTTON_SIZE

            pil_image = Image.open(path).resize((s, s))

            self.__image_cache[path] = ImageTk.PhotoImage(pil_image)

        return self.__image_cache[path]

    def __display_board(self,
                        callback: Callable[[int, int], None]) -> None:
        '''
        Packs the board onto the end of the current screen. This
        does NOT clear the screen!

        :param callback: The function which button presses will
            call.
        '''

        class Ret:
            '''
            An internal callable class for board button
            callbacks.
            '''

            def __init__(self,
                         x: int,
                         y: int,
                         c: Callable[[int, int], None]) -> None:
                self.__x = x
                self.__y = y
                self.__c = c

            def __call__(self) -> None:
                self.__c(self.__x, self.__y)

        for y in range(self.__board.height - 1, -1, -1):

            row: tk.Frame = tk.Frame(self.__root)

            for x in range(self.__board.width):

                path: str = self.__piece_to_image_path(self.__board.get(x, y))
                image: tk.PhotoImage = self.__get_image(path)

                tk.Button(row,
                          command=Ret(x, y, callback),
                          image=image,
                          border=0,
                          width=32,
                          height=32).pack(side='left')
            row.pack()

    def __board_movement_callback(self, x: int, y: int) -> None:
        '''
        This is a callback function for board buttons. The first
        time it is called, it loads into self.__from_selection.
        The second time, it loads into self.__to_selection and
        calls the given callback function. Then, it resets its
        member variables.

        :param x: The x-coord of the board button pressed.
        :param y: The y-coord of the board button pressed.
        '''

        if self.__from_selection is None:
            self.__from_selection = (x, y)
            return

        self.__to_selection = (x, y)

        self.__check_move()

        self.__from_selection = None
        self.__to_selection = None

    def __board_setup_callback(self, x: int, y: int) -> None:
        '''
        This is a callback function for board buttons. This is
        used for setting up the board.

        :param x: The x-coord of the board button pressed.
        :param y: The y-coord of the board button pressed.
        '''

        if self.__from_selection is None:
            self.__from_selection = (x, y)
            return

        self.__to_selection = (x, y)

        self.__check_move()

        self.__from_selection = None
        self.__to_selection = None

    def __home_screen(self) -> None:
        '''
        The host/connect screen of the app.
        '''

        self.__clear()

        tk.Label(self.__root, text='Stratego').pack()

        tk.Button(self.__root,
                  text='Host Game',
                  command=self.__host_game_screen).pack()
        tk.Button(self.__root,
                  text='Join Game',
                  command=self.__join_game_screen).pack()

        tk.Button(self.__root, text='Info', command=self.__info_screen).pack()
        tk.Button(self.__root, text='Quit', command=self.__quit).pack()

        # Permanent keybindings
        self.__bind('h', self.__host_game_screen)
        self.__bind('j', self.__join_game_screen)

        # Debugging keybindings
        self.__bind('s', self.__setup_screen)
        self.__bind('y', self.__your_turn_screen)
        self.__bind('t', self.__their_turn_screen)
        self.__bind('w', self.__win_screen)
        self.__bind('l', self.__lose_screen)
        self.__bind('e', self.__error_screen)

        self.__root.mainloop()

    def __info_screen(self) -> None:
        '''
        The information screen.
        '''

        self.__clear()

        tk.Label(self.__root,
                 text='2024, N Barnaik, J Dehmel, K Eckhart').pack()
        tk.Label(self.__root,
                 text='This software was developed as an exercise,\n' +
                      'and the authors lay no claim to the copyright\n' +
                      'of Stratego. This software is not to be used\n' +
                      'commercially.'
                 ).pack()

        tk.Button(self.__root,
                  text='Home',
                  command=self.__home_screen).pack()
        tk.Button(self.__root,
                  text='Quit',
                  command=self.__quit).pack()

    def __bind(self, sequence: str, event: Callable[[], None]) -> None:
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
            child.destroy()  # Metal

        # Unbind all keybindings registered herein
        for key in self.__keybindings:
            self.__root.unbind(key)

        # Set title
        if self.__color:
            self.__root.title(self.__color)

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
            tk.Label(self.__root, text='Waiting for other player...').pack()
            self.__root.update()

            # Make API call and wait
            self.__networking.host_wait_for_join()

            # When API call is done, advance to next screen
            self.__color = 'RED'
            self.__setup_screen(True)

        tk.Button(self.__root,
                  text='Host This Game',
                  command=host_game_callback).pack()
        self.__bind('<Return>', host_game_callback)

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
            result: int = self.__networking.join_game(ip_str,
                                                      port_int,
                                                      password_str)

            if result == 0:
                # When API call is done, advance to next screen
                self.__color = 'BLUE'
                self.__setup_screen(True)

            else:
                tk.Label(self.__root,
                         text=f'Failed to connect (code: {result}).').pack()

        tk.Button(self.__root,
                  text='Join This Game',
                  command=join_game_callback).pack()
        self.__bind('<Return>', join_game_callback)

    def __setup_left_to_place(self) -> None:
        '''
        '''

        # 6 Bombs
        for _ in range(6):
            self.__left_to_place.append(p.Bomb(self.__color))

        # 8 Scouts
        for _ in range(8):
            self.__left_to_place.append(p.Scout(self.__color))

        # 5 Miners
        for _ in range(5):
            self.__left_to_place.append(p.Miner(self.__color))

        # 1 Marshal
        # 1 Spy
        # 1 Flag
        # 1x9
        # 2x8
        self.__left_to_place += [p.Marshal(self.__color),
                                 p.Spy(self.__color),
                                 p.Flag(self.__color),
                                 p.Troop(self.__color, 9),
                                 p.Troop(self.__color, 8),
                                 p.Troop(self.__color, 8)]

        # 3x7
        for _ in range(3):
            self.__left_to_place.append(p.Troop(self.__color, 7))

        # 4x6
        for _ in range(4):
            self.__left_to_place.append(p.Troop(self.__color, 6))

        # 4x5
        for _ in range(4):
            self.__left_to_place.append(p.Troop(self.__color, 5))

        # 4x4
        for _ in range(4):
            self.__left_to_place.append(p.Troop(self.__color, 4))

        assert len(self.__left_to_place) == 40

    def __setup_screen(self, first: bool = False) -> None:
        '''
        The board setup screen.

        :param first: Only true the first time this function is
            called.
        '''

        self.__clear()

        # Setup pieces left to place if need be
        if first:
            self.__setup_left_to_place()

        # If done w/ setup, continue to play
        if len(self.__left_to_place) == 0:

            if self.__color == 'RED':
                self.__your_turn_screen()

            else:
                self.__their_turn_screen()

            return

        tk.Label(self.__root, text='Set up your pieces.').pack()

        self.__display_board(self.__board_setup_callback)

    def __your_turn_screen(self) -> None:
        '''
        Screen allowing our player to make a move.
        '''

        # Update screen
        self.__clear()
        tk.Label(self.__root, text='Your turn.').pack()

        self.__display_board(self.__board_movement_callback)

    def __check_move(self) -> None:

        assert self.__from_selection
        assert self.__to_selection

        # Check validity
        try:
            state = self.__board.move(self.__color,
                                      self.__from_selection,
                                      self.__to_selection)

        except b.InvalidMoveError:
            self.__your_turn_screen()
            return

        # Send to other player
        self.__board, state = self.__networking.sync_game(self.__board, state)

        # Check game state
        if state == 'WIN':
            self.__win_screen()
        elif state == 'LOSE':
            self.__lose_screen()
        elif state == 'HALT':
            self.__error_screen()

    def __their_turn_screen(self) -> None:
        '''
        Waiting screen while the other player moves.
        '''

        # Update screen
        self.__clear()
        tk.Label(self.__root, text='Thier turn; Waiting.').pack()

        self.__display_board(lambda _, __: None)
        self.__root.update()

        # Wait for move recv
        self.__board, state = self.__networking.sync_game(self.__board, '')

        # Check game state
        if state == 'WIN':
            self.__win_screen()
        elif state == 'LOSE':
            self.__lose_screen()
        elif state == 'HALT':
            self.__error_screen()

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

        tk.Label(self.__root, text='Error: Connection terminated.').pack()

        tk.Button(self.__root,
                  text='Play Again',
                  command=self.__home_screen).pack()
        tk.Button(self.__root,
                  text='Quit',
                  command=self.__quit).pack()
