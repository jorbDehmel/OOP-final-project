'''
Defines a Stratego GUI using tkinter. This class should
aggregate the board and networking. This is what should be
presented to the user.
'''

from random import shuffle
import tkinter as tk
from typing import Optional, List, Callable, Tuple, Dict, Literal

import stratego
import stratego.board as b
import stratego.network
import stratego.pieces as p


def resize_image(img: tk.PhotoImage, w: int, h: int) -> tk.PhotoImage:
    '''
    Resizes a tk.PhotoImage object. There is a better way to do
    this, but this is the only way that works with mypy.
    :param img: The image to resize.
    :param w: The desired width.
    :param h: The desired height.
    :returns: The resized image.
    '''

    old_w: int = img.width()
    old_h: int = img.height()

    out: tk.PhotoImage = tk.PhotoImage(width=w, height=h)

    # Skip trivial case
    if old_w and old_h:

        # Iterate over pixels
        for x in range(w):
            for y in range(h):

                # Get pixel at the corresponding source coords
                old_x: int = int(x * old_w / w)
                old_y: int = int(y * old_h / h)
                result = img.get(old_x, old_y)

                # Format in desired way
                rgb: str = f'#{hex(result[0])[2:]}{hex(result[1])[2:]}' + \
                           f'{hex(result[2])[2:]}'

                # Write pixel
                out.put(rgb, (x, y))
                out.transparency_set(x, y, img.transparency_get(old_x, old_y))

    return out


ScreenType = Literal['HOME', 'INFO', 'WIN', 'LOSE', 'ERROR',
                     'SETUP', 'HOST_GAME', 'JOIN_GAME',
                     'YOUR_TURN', 'THEIR_TURN', '']


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

    @classmethod
    def clear_instance(cls) -> None:
        '''
        Reset this singleton class.
        '''

        if cls.__INSTANCE is not None:
            del cls.__INSTANCE
            cls.__INSTANCE = None

    def press_key(self, key: str) -> None:
        '''
        Simulates the given keypress, given that it is bound.
        :param key: The key event code.
        '''

        assert key in self.__keybindings
        self.__keybindings[key]()

    def __init__(self) -> None:
        '''
        Initialize the GUI window, given that none already
        exist.
        '''

        assert type(self).__INSTANCE is None, 'Cannot reinstantiate singleton'

        # Used for testing purposes
        self.__screen: ScreenType = ''

        # TK root object; This is the screen we write in.
        self.__root: tk.Tk = tk.Tk()

        # Global configuration options.
        self.__root.configure(bg='white')
        self.__root.option_add('*Background', 'white')
        self.__root.option_add('*Font', 'Times 16')
        # self.__root.geometry("448x448")

        # Game management objects
        self.__board: b.Board = b.Board.get_instance()
        self.__networking: stratego.network.StrategoNetworker = \
            stratego.network.StrategoNetworker()

        # Game state objects
        self.__title: str = 'Stratego'
        self.__color: Literal['BLUE', 'RED'] = 'RED'
        self.__from_selection: Optional[Tuple[int, int]] = None
        self.__to_selection: Optional[Tuple[int, int]] = None
        self.__left_to_place: List[p.Piece] = []

        # Internal optimizations and bookkeeping
        self.__keybindings: Dict[str, Callable[[], None]] = {}
        self.__image_cache: Dict[str, tk.PhotoImage] = {}

        # This keybinding is not tracked and thus not erased
        self.__root.bind('q', lambda _: self.__quit())

        # Set title
        self.__root.title(self.__title)

        # Initiate game
        self.__home_screen()

    @property
    def screen(self) -> ScreenType:
        '''
        Getter for the self.__screen variable.
        '''

        return self.__screen

    @screen.setter
    def screen(self, to: ScreenType) -> None:
        '''
        Moves to the given string, as long as it exists.
        '''

        cases: Dict[ScreenType, Callable[[], None]] = {
            'HOME': self.__home_screen,
            'INFO': self.__info_screen,
            'WIN': self.__win_screen,
            'LOSE': self.__lose_screen,
            'ERROR': self.__error_screen,
            'SETUP': self.__setup_screen,
            'HOST_GAME': self.__host_game_screen,
            'JOIN_GAME': self.__join_game_screen,
            'YOUR_TURN': self.__your_turn_screen,
            'THEIR_TURN': self.__their_turn_screen
        }

        assert to in cases
        cases[to]()

    @property
    def color(self) -> Literal['RED', 'BLUE']:
        '''
        Getter for the color of the player.
        '''

        return self.__color

    @color.setter
    def color(self, to: Literal['RED', 'BLUE']) -> None:
        '''
        Setter for the color of the player.
        '''

        self.__color = to

    @property
    def board(self) -> b.Board:
        '''
        Returns the board.
        '''

        return self.__board

    def __get_image(self, piece: b.Square) -> tk.PhotoImage:
        '''
        :param piece: The piece to load the image from.
        :returns: A tk-compatible version of that image.
        '''

        path: str = 'stratego/images/blank.png'

        if piece is not None:

            if isinstance(piece, b.LakeSquare):
                path = 'stratego/images/lake.png'

            elif isinstance(piece, p.Piece):

                if piece.color != self.__color:
                    path = f'stratego/images/{piece.color}_blank.png'

                else:
                    try:
                        path = f'stratego/images/{piece.color}_{repr(piece)}.png'
                    except TypeError:
                        path = f'stratego/images/{piece.color}_blank.png'

        if path not in self.__image_cache:
            raw: tk.PhotoImage = tk.PhotoImage(file=path)
            self.__image_cache[path] = resize_image(raw, self._BUTTON_SIZE, self._BUTTON_SIZE)

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
                self.x = x
                self.y = y
                self.c = c

            def __call__(self) -> None:
                self.c(self.x, self.y)

        for y in range(self.__board.height - 1, -1, -1):

            row: tk.Frame = tk.Frame(self.__root)

            for x in range(self.__board.width):

                image: tk.PhotoImage = self.__get_image(self.__board.get(x, y))

                tk.Button(row,
                          command=Ret(x, y, callback),
                          image=image,
                          border=0,
                          width=32,
                          height=32).pack(side='left')
            row.pack()

    def __bind(self, sequence: str, event: Callable[[], None]) -> None:
        '''
        Bind the given sequence to the given callable. The
        callable will be passed no arguments. Any keybinding
        registered in this way will be erased by the clear()
        method.
        '''

        self.__root.bind(sequence, lambda _: event())
        self.__keybindings[sequence] = event

    def quit(self) -> None:
        '''
        Kills the app.
        '''

        self.__quit()

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

        self.__keybindings = {}
        self.__screen = ''

        # Set title
        self.__root.title(self.__title)

        # Empty widget to maintain width
        tk.Label(self.__root, height=0, width=25).pack()

    def __home_screen(self) -> None:
        '''
        The host/connect screen of the app.
        '''

        self.__clear()
        self.__screen = 'HOME'

        tk.Label(self.__root, text='\nStratego\n\n').pack()

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

        self.__root.mainloop()

    def __info_screen(self) -> None:
        '''
        The information screen.
        '''

        self.__clear()
        self.__screen = 'INFO'

        tk.Label(self.__root,
                 text='2024\nN Barnaik, J Dehmel, K Eckhart').pack()
        tk.Label(self.__root,
                 text='This software was developed as\n' +
                      'an exercise, and the authors lay\n' +
                      'no claim to the copyright of\n' +
                      'Stratego. This software is not\n' +
                      'to be used commercially.'
                 ).pack()

        tk.Button(self.__root,
                  text='Home',
                  command=self.__home_screen).pack()
        tk.Button(self.__root,
                  text='Quit',
                  command=self.__quit).pack()

    def __host_game_screen(self) -> None:
        '''
        The screen which allows you to initiate hosting a game.
        '''

        # Clear screen
        self.__clear()
        self.__screen = 'HOST_GAME'

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
            if ip_str == '':
                ip_str = '127.0.0.1'

            port_str: str = port.get()
            if port_str == '':
                port_str = '12345'

            port_int: int = int(port_str)
            password: str = ''

            while password == '':
                try:
                    password = self.__networking.host_game(ip_str, port_int)
                except OSError:
                    port_int += 1
                    password = ''

            # Display waiting text
            self.__clear()
            tk.Label(self.__root,
                     text=f'IP: {ip_str}\nPort: {port_int}\n'
                          + f'Password: {password}').pack()
            tk.Label(self.__root, text='Waiting for other player...').pack()
            self.__root.update()

            # Make API call and wait
            self.__networking.host_wait_for_join()

            # When API call is done, advance to next screen
            self.__color = 'RED'

            self.__setup_screen()

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
        self.__screen = 'JOIN_GAME'

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
            password_str: str = password.get()

            if password_str == '':
                return

            ip_str: str = ip.get()
            if ip_str == '':
                ip_str = '127.0.0.1'

            port_str: str = port.get()
            if port_str == '':
                port_str = '12345'

            port_int: int = int(port_str)

            # Make API call and wait
            result: int = self.__networking.join_game(ip_str,
                                                      port_int,
                                                      password_str)

            if result == 0:
                # When API call is done, advance to next screen
                self.__color = 'BLUE'

                self.__setup_screen()

            else:
                tk.Label(self.__root,
                         text=f'Failed to connect (code: {result}).').pack()

        tk.Button(self.__root,
                  text='Join This Game',
                  command=join_game_callback).pack()
        self.__bind('<Return>', join_game_callback)

    def __setup_left_to_place(self) -> None:
        '''
        Sets up the self.__left_to_place variable, which is a
        list of all the pieces which have not yet been placed
        by this user.
        '''

        # Fetch all pieces
        self.__left_to_place = self.__board.all_pieces(self.__color)

        # Setup other color placeholder pieces
        if self.__color == 'BLUE':
            self.__board.fill((0, 0), (10, 4), p.Bomb('RED'))
        else:
            self.__board.fill((0, 6), (10, 10), p.Bomb('BLUE'))

    def __randomize_all(self) -> None:
        '''
        Randomizes all remaining pieces
        '''

        shuffle(self.__left_to_place)

        if self.__color == 'RED':
            self.__board.fill((0, 0),
                              (10, 4),
                              lambda _, __: self.__left_to_place.pop())

        else:
            self.__board.fill((0, 6),
                              (10, 10),
                              lambda _, __: self.__left_to_place.pop())

        self.__setup_screen()

    def __first_sync(self) -> None:
        '''
        Sync the two boards and begin play. This is to be called
        when setup screen is done.
        '''

        if self.__color == 'RED':

            # Recv
            their_board, _ = self.__networking.recv_game()
            for y in range(0, 4):
                for x in range(0, 10):
                    their_board.set_piece(x, y, self.__board.get(x, y))
            self.__board = their_board

            # Send
            self.__networking.send_game(self.__board, 'GOOD')

            self.__your_turn_screen()
            return

        self.__clear()
        tk.Label(self.__root, text='Waiting...').pack()
        self.__display_board(lambda _, __: None)
        self.__root.update()

        # Send
        self.__networking.send_game(self.__board, 'GOOD')

        # Recv
        their_board, _ = self.__networking.recv_game()
        for y in range(6, 10):
            for x in range(0, 10):
                their_board.set_piece(x, y, self.__board.get(x, y))
        self.__board = their_board

        self.__their_turn_screen()

    def __setup_screen(self) -> None:
        '''
        The board setup screen.
        '''

        def board_setup_callback(x: int, y: int) -> None:
            '''
            This is a callback function for board buttons. This is
            used for setting up the board.

            :param x: The x-coord of the board button pressed.
            :param y: The y-coord of the board button pressed.
            '''

            # Red is able to place pieces in the TOP 4 rows
            if self.__color == 'RED':
                if y not in range(0, 4) or self.__board.get(x, y) is not None:
                    print('Invalid placement!')
                    return

            # Blue is able to place pieces in the BOTTOM 4 rows
            else:
                if y not in range(6, 10) or self.__board.get(x, y) is not None:
                    print('Invalid placement!')
                    return

            self.__board.set_piece(x, y, self.__left_to_place.pop(0))

            # If done w/ setup, continue to play
            if len(self.__left_to_place) == 0:
                self.__first_sync()
                return

            self.__setup_screen()

        self.__clear()
        self.__screen = 'SETUP'

        if len(self.__left_to_place) == 0:
            self.__setup_left_to_place()

        tk.Label(self.__root, text='Click to place this piece:').pack()

        image: tk.PhotoImage = self.__get_image(self.__left_to_place[0])

        tk.Label(self.__root,
                 image=image,
                 border=0,
                 width=32,
                 height=32).pack()

        tk.Button(self.__root,
                  text='Randomize all',
                  command=self.__randomize_all).pack()

        self.__display_board(board_setup_callback)

    def __your_turn_screen(self) -> None:
        '''
        Screen allowing our player to make a move.
        '''

        def board_movement_callback(x: int, y: int) -> None:
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

        try:
            # Update screen
            self.__clear()
            self.__screen = 'YOUR_TURN'
            tk.Label(self.__root, text='Your turn.').pack()

            self.__display_board(board_movement_callback)

        except ValueError:
            self.__error_screen()

    def __check_move(self) -> None:

        assert self.__from_selection
        assert self.__to_selection

        # Check validity
        try:

            state = self.__board.move(self.__color,
                                      self.__from_selection,
                                      self.__to_selection)

        except b.InvalidMoveError:
            print('Invalid move')
            self.__your_turn_screen()
            return

        try:

            # Send to other player
            self.__networking.send_game(self.__board, state)

            # Check game state
            if state == self.__color:
                self.__win_screen()

            elif state != 'GOOD':
                self.__lose_screen()

            else:
                self.__their_turn_screen()

        except ValueError:
            self.__error_screen()

    def __their_turn_screen(self) -> None:
        '''
        Waiting screen while the other player moves.
        '''

        try:

            # Update screen
            self.__clear()
            self.__screen = 'THEIR_TURN'
            tk.Label(self.__root, text='Thier turn; Waiting.').pack()

            self.__display_board(lambda _, __: None)
            self.__root.update()

            # Wait for move recv
            self.__board, state = self.__networking.recv_game()

            # Check game state
            if state == self.__color:
                self.__win_screen()

            elif state != 'GOOD':
                self.__lose_screen()

            else:
                self.__your_turn_screen()

        except ValueError:
            self.__error_screen()

    def __win_screen(self) -> None:
        '''
        Shown when our player wins.
        '''

        self.__clear()
        self.__screen = 'WIN'

        self.__networking.close_game()

        tk.Label(self.__root,
                 image=self.__get_image(p.Flag(self.__color))).pack()

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
        self.__screen = 'LOSE'

        self.__networking.close_game()

        tk.Label(self.__root,
                 image=self.__get_image(p.Bomb(self.__color))).pack()

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
        self.__screen = 'ERROR'

        self.__networking.close_game()

        tk.Label(self.__root, text='Error: Connection terminated.').pack()

        tk.Button(self.__root,
                  text='Play Again',
                  command=self.__home_screen).pack()
        tk.Button(self.__root,
                  text='Quit',
                  command=self.__quit).pack()
