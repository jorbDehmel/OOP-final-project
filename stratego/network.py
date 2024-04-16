'''
Network operations for OOP Stratego. Should send the game state
from GUI to GUI via JSON. This could take the form of a
singleton API handler wrapper class.
'''

from typing import Tuple, Optional
import pickle
import socket
import random
from stratego.board import Board


class StrategoNetworker:
    '''
    Handles networking operations for Stratego. This is
    aggregated by the GUI class in stratego.gui.
    '''

    __SIZE_STR_MAX_SIZE: int = 16
    __STATE_STR_MAX_SIZE: int = 8
    __PASSWORD_SIZE: int = 4
    __INSTANCE: Optional['StrategoNetworker'] = None

    @staticmethod
    def is_terminal_state(cur_state: str) -> bool:
        '''
        Returns whether or not this state indicates cessation of
        the game.

        :param cur_state: The current game state.
        :returns: True if the game is now over.
        '''

        if cur_state in ('RED', 'BLUE', 'HALT'):
            return True

        return False

    @classmethod
    def get_instance(cls) -> 'StrategoNetworker':
        '''
        Return the instance of this class, creating it if need
        be.

        :returns: The instance of this class.
        '''

        if cls.__INSTANCE is None:
            cls.__INSTANCE = StrategoNetworker()

        return cls.__INSTANCE

    def __init__(self) -> None:
        '''
        Create infrastructure, but do NOT open socket yet.
        '''

        assert type(self).__INSTANCE is None, 'Cannot re-instantiate singleton'

        self.__is_connected: bool = False

        self.__host_socket: Optional[socket.socket] = None
        self.__client_socket: Optional[socket.socket] = None

        self.__password: str = ''

    def host_game(self, ip: str, port: int) -> str:
        '''
        Opens a game on the given IPv4 and port.

        :param ip: The IPv4 address to host on. Probably
            localhost.
        :param port: The port to listen on.
        :returns: The join password (randomly generated).
        '''

        self.__host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host_socket.bind((ip, port))

        legal_chars: str = '0123456789ABCDEF'
        self.__password = ''

        for _ in range(type(self).__PASSWORD_SIZE):
            self.__password += random.choice(legal_chars)

        return self.__password

    def host_wait_for_join(self) -> None:
        '''
        Waits until another player joins. When they join, asks
        for a password. If they get it wrong, goes back to
        waiting.
        '''

        assert self.__host_socket is not None

        while not self.__is_connected:
            try:
                self.__host_socket.listen(1)
                self.__client_socket, _ = self.__host_socket.accept()

                self.__is_connected = True

                s: int = type(self).__PASSWORD_SIZE
                b: bytes = self.__client_socket.recv(s)

                password: str = b.decode('UTF-8')

                if password != self.__password:
                    self.__send_game_state('HALT')

                    print('Failed password attempt.')
                    self.__is_connected = False

                else:
                    self.__send_game_state('GOOD')

            except OSError as e:
                print(f'Caught OSError {e}')

    def join_game(self, ip: str, port: int, password: str) -> int:
        '''
        Attempts to join the game at the given IPv4 and port.

        :param ip: The IPv4 address to attempt to connect to.
        :param port: The port to attempt to connect to.
        :param password: The join password from the host.
        :returns: 0 on success, 1 on socket failure, 2 on
            password failure.
        '''

        self.__is_connected = False

        # Connect to server
        try:
            self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__client_socket.connect((ip, port))
        except socket.error as e:
            print(f'Caught socket error {e}')
            return 1

        # Send password
        self.__is_connected = True
        self.__client_socket.send(bytes(password, 'UTF-8'))

        state: str = self.__recv_game_state()

        if state != 'GOOD':
            self.__client_socket.close()
            self.__client_socket = None
            self.__is_connected = False
            return 2

        self.__is_connected = True

        return 0

    def close_game(self) -> None:
        '''
        Closes the connection.
        '''

        try:
            if self.__client_socket is not None:
                self.__send_game_state('HALT')
                self.__client_socket.close()
        except socket.error:
            pass

    def send_game(self, board: Board, state: str) -> None:
        '''
<<<<<<< HEAD
=======
        Send the board and state.
>>>>>>> origin/main
        '''

        self.__send_board(board)
        self.__send_game_state(state)

    def recv_game(self) -> Tuple[Board, str]:
        '''
        Read the board and state from the socket.
        '''

        out_board: Board = self.__recv_board()
        out_state: str = self.__recv_game_state()

        return (out_board, out_state)

    # Helper functions

    def __send_board(self, to_send: Board) -> None:
        '''
        Serializes and sends the given board over the existing
        connection.

        :param to_send: The board to send.
        '''

        assert self.__is_connected, 'Cannot send before connecting'
        assert self.__client_socket, 'Cannot send before connecting'

        serialized: bytes = pickle.dumps(to_send)

        # Get size in bytes
        size: int = len(serialized)

        # Prepare str of length type(self).__SIZE_STR_MAX_SIZE of size
        # padded on RIGHT side w/ SPACES
        size_str: str = str(size)
        size_str += (' ' * (type(self).__SIZE_STR_MAX_SIZE - len(size_str)))

        # Send size
        self.__client_socket.send(bytes(size_str, 'UTF-8'))

        # Send board
        self.__client_socket.send(serialized)

    def __recv_board(self) -> Board:
        '''
        Receives and returns a board from the existing
        connection. Hangs until it receives the board.

        :returns: The received board.
        '''

        assert self.__is_connected, 'Cannot recv before connecting'
        assert self.__client_socket, 'Cannot recv before connecting'

        size_str: str = self.__client_socket.recv(type(self).__SIZE_STR_MAX_SIZE).decode('UTF-8')

        serialized: bytes = self.__client_socket.recv(int(size_str))

        out: Board = pickle.loads(serialized)

        return out

    def __send_game_state(self, state: str) -> None:
        '''
        Sends the given game state.

        :param state: The current game state.
        '''

        assert self.__is_connected, 'Cannot send before connecting'
        assert self.__client_socket, 'Cannot send before connecting'

        to_send: str = state
        to_send += (' ' * (type(self).__STATE_STR_MAX_SIZE - len(to_send)))

        self.__client_socket.send(bytes(to_send, 'UTF-8'))

    def __recv_game_state(self) -> str:
        '''
        Receives the game state.

        :returns: The received game sate.
        '''

        assert self.__is_connected, 'Cannot recv before connecting'
        assert self.__client_socket, 'Cannot recv before connecting'

        b: bytes = self.__client_socket.recv(type(self).__STATE_STR_MAX_SIZE)
        state: str = b.decode('UTF-8').strip(' ')

        return state
