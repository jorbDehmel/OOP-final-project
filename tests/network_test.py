'''
Tests network operations for Stratego.
'''

import unittest
from unittest import mock
from typing import Tuple
import multiprocessing as mp
from multiprocessing import connection as mp_connect
from stratego import network as n


class MockSocket:
    '''
    For replacing sockets when testing.
    '''

    def __init__(self, _sock_type: object, _sock_proto: object) -> None:
        '''
        Dummy function.
        '''

    def accept(self) -> Tuple['MockSocket', None]:
        '''
        Dummy function.
        '''

        # return (self, None)

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

        # self._pipe.close()

    def send(self, data: bytes) -> None:
        '''
        Dummy function.
        '''

        # assert isinstance(data, bytes)
        # self._pipe.send(data)

    def recv(self, size: int) -> None:
        '''
        Dummy function.
        '''

        # data = self._pipe.recv()
        # assert isinstance(data, bytes) and len(data) == size
        # return data

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

    def host_test(self) -> None:
        '''
        Tests the host_game function
        '''
        # with (mock.patch('random.choice', mock.Mock(return_value='0')), mock('socket.socket')):
        #     self.assertEqual(n.StrategoNetworker.host_game('127.0.0.1', 1234), '0000')

    def test_host_wait(self) -> None:
        """Tests the host_wait_for_join function
        """
        

    def join_test(self) -> None:
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
