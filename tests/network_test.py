'''
Tests network operations for Stratego.
'''

import unittest
# from unittest import mock
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


def run_in_network_context(server_fn, client_fn) -> None:
    '''
    Run the given functions in a network context.
    '''

    def main(pipe, test_fn) -> int:
        '''
        Main function for staging purposes.
        '''

        # with mock.patch('socket.socket', new=MockSocket):
        #     MockSocket._pipe = pipe  # TODO: Fix this!
        #     test_fn()

        # return 0

    (server_pipe, client_pipe) = mp.Pipe()
    server_process = mp.Process(target=main, args=(server_pipe, server_fn))
    client_process = mp.Process(target=main, args=(client_pipe, client_fn))
    server_process.start()
    client_process.start()

    try:
        running_process = [server_process, client_process]
        while len(running_process) > 0:
            done = mp_connect.wait([x.sentinel for x in running_process])
            for x in done:
                for i, _ in enumerate(running_process):
                    if x == running_process[i].sentinel:
                        if running_process[i].exitcode is not None:
                            assert running_process[i].exitcode == 0
                        del running_process[i]
                        break

    finally:
        server_process.kill()
        client_process.kill()


class TestStrategoNetworking(unittest.TestCase):
    '''
    Tests the stratego networking class.
    '''

    def test_init(self) -> None:
        '''
        Tests the init function.
        '''
        n.StrategoNetworker.get_instance()

    def test_host_join(self) -> None:
        '''
        Tests the host game and join game function.
        '''

        def host_test(pass_sidechannel) -> None:
            '''
            Host function
            '''

            def main() -> int:
                '''
                Dummy main
                '''

                # nonlocal pass_sidechannel
                # net = n.StrategoNetworker.get_instance()
                # password = net.host_game('', 0)
                # pass_sidechannel.send(password)
                # net.host_wait_for_join()

                # return 0

            return main

        def join_test(pass_sidechannel) -> None:
            '''
            Join function
            '''

            def main() -> int:
                '''
                Dummy main
                '''

                # nonlocal pass_sidechannel
                # password = pass_sidechannel.recv()
                # net = n.StrategoNetworker.get_instance()
                # assert net.join_game('', 0, password) == 0

                # return 0

            return main

        (pass_sidechannel_send, pass_sidechannel_recv) = mp.Pipe()
        run_in_network_context(host_test(pass_sidechannel_send), join_test(pass_sidechannel_recv))

    def test_send_board(self) -> None:
        '''
        Tests the send_board function.
        '''

    def test_recv_board(self) -> None:
        '''
        Tests the recv_board function.
        '''

    def test_integration(self) -> None:
        '''
        Tests all the above functions together.
        '''
