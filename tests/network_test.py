'''
Tests network operations for Stratego.
'''

import unittest
from unittest import mock
from stratego import network as n
import multiprocessing as mp
from multiprocessing import connection as mp_connect

class MockSocket:
    def __init__(self, _sock_type: object, _sock_proto: object):
        pass

    def accept(self):
        return (self, None)

    def bind(self, _addr: object):
        pass

    def listen(self, _backlog: object):
        pass

    def connect(self, _addr: object):
        pass

    def close(self):
        self._pipe.close()

    def send(self, data: bytes):
        assert isinstance(data, bytes)
        self._pipe.send(data)

    def recv(self, size: int):
        data = self._pipe.recv()
        assert isinstance(data, bytes) and len(data) == size
        return data

def run_in_network_context(server_fn, client_fn):
    def main(pipe, test_fn):
        with mock.patch('socket.socket', new=MockSocket):
            MockSocket._pipe = pipe
            test_fn()

    (server_pipe, client_pipe) = mp.Pipe()
    server_process = mp.Process(target = main, args=(server_pipe, server_fn))
    client_process = mp.Process(target = main, args=(client_pipe, client_fn))
    server_process.start()
    client_process.start()
    try:
        running_process = [server_process, client_process]
        while len(running_process) > 0:
            done = mp_connect.wait([x.sentinel for x in running_process])
            for x in done:
                for i in range(0, len(running_process)):
                    if x == running_process[i].sentinel:
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
        def host_test(pass_sidechannel):
            def main():
                nonlocal pass_sidechannel
                net = n.StrategoNetworker.get_instance()
                password = net.host_game('', 0)
                pass_sidechannel.send(password)
                net.host_wait_for_join()
            return main

        def join_test(pass_sidechannel):
            def main():
                nonlocal pass_sidechannel
                password = pass_sidechannel.recv()
                net = n.StrategoNetworker.get_instance()
                assert net.join_game('', 0, password) == 0
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
        pass
