'''
Tests network operations for Stratego.
'''

import unittest
from unittest import mock
import socket
from typing import Tuple, Dict, Any
from stratego import network as n


class MockSocket:
    '''
    For replacing sockets when testing.
    '''

    kwargs: Dict[str, Any] = {}

    def __init__(self, *_, **kwargs) -> None:
        '''
        Dummy function.
        '''

        type(self).kwargs |= kwargs

    def accept(self) -> Tuple['MockSocket', None]:
        '''
        Dummy function.
        '''

        return (self, None)

    def bind(self, _addr: object) -> None:
        '''
        Dummy function.
        '''

    def listen(self, _backlog: object) -> None:
        '''
        Dummy function.
        '''

    def connect(self, _addr: object) -> None:
        '''
        Dummy function.
        '''

    def close(self) -> None:
        '''
        Dummy function.
        '''

    def send(self, data: bytes) -> None:
        '''
        Dummy function.
        '''

    def recv(self, _: int) -> bytes:
        '''
        Dummy function.
        '''

        return type(self).kwargs['recv'].pop(0)


class TestStrategoNetworking(unittest.TestCase):
    '''
    Tests the stratego networking class.
    '''

    def test_is_terminal_state(self) -> None:
        """Tests the is_terminal_state function
        """
        assert n.StrategoNetworker.is_terminal_state('RED')
        assert n.StrategoNetworker.is_terminal_state('BLUE')
        assert n.StrategoNetworker.is_terminal_state('HALT')
        assert not n.StrategoNetworker.is_terminal_state('')

    def test_init(self) -> None:
        '''
        Tests the init function.
        '''
        n.StrategoNetworker.get_instance()

    def test_host(self) -> None:
        '''
        Tests the host_game function
        '''

        with (mock.patch('random.choice', mock.Mock(return_value='0')),
              mock.patch('socket.socket')):

            n.StrategoNetworker.clear_instance()
            net: n.StrategoNetworker = n.StrategoNetworker.get_instance()

            password: str = net.host_game('127.0.0.1', 12345)
            self.assertEqual(password, '0000')

            n.StrategoNetworker.clear_instance()

    def test_host_wait(self) -> None:
        """Tests the host_wait_for_join function
        """

        # Test valid join, password error
        with (mock.patch('random.choice', mock.Mock(return_value='0')),
              mock.patch('socket.socket', MockSocket) as fake_sock):

            fake_sock.kwargs['recv'] = [b'0001', b'0000']

            n.StrategoNetworker.clear_instance()
            net: n.StrategoNetworker = n.StrategoNetworker.get_instance()

            password: str = net.host_game('127.0.0.1', 12345)
            self.assertEqual(password, '0000')

            net.host_wait_for_join()
            net.close_game()

            n.StrategoNetworker.clear_instance()

        def dummy_fn(_, __: int) -> None:
            '''
            Dummy function
            '''

            raise OSError()

        def dummy_close_fn(_) -> None:
            '''
            Dummy function
            '''

            raise socket.error

        # Test throwing error
        with (mock.patch.object(MockSocket, 'recv', dummy_fn),
              mock.patch.object(MockSocket, 'close', dummy_close_fn),
              mock.patch('random.choice', mock.Mock(return_value='0')),
              mock.patch('socket.socket', MockSocket) as fake_sock):

            n.StrategoNetworker.clear_instance()
            net: n.StrategoNetworker = n.StrategoNetworker.get_instance()

            net.host_game('127.0.0.1', 12345)
            net.host_wait_for_join()

            net.close_game()

            n.StrategoNetworker.clear_instance()

    def test_join(self) -> None:
        '''
        Tests the join_game function
        '''

    def test_send_board(self) -> None:
        '''
        Tests the send_board function.
        '''

    def test_recv_board(self) -> None:
        '''
        Tests the recv_board function.
        '''
