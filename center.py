import functools
import time
import sys
import getopt
from inspect import signature
from util import Util, Logger
from tornado_tcpserver import TornadoTCPServerHolder
from tornado_tcpclient import TornadoTCPClientHolder

# should be run with python version >= 3.5
assert sys.version_info >= (3, 5)
HELP_MSG = open('USAGE').read()


class TornadoCenter(Logger):
    """
    Center Handler
    """
    def __init__(self):
        """
        Initialization
        """
        Logger.__init__(self, 'TornadoCenter')
        self._log('Welcome to TornadoCenter!!!')
        self._cmd_state = {
            'exit': self._exit,
            'help': self._help,
            'server': {
                'start': self._start_server,
                'stop': self._stop_server,
                'params': self._show_server_params,
                'status': self._show_server_status
            },
            'client': {
                'start': self._start_client,
                'stop': self._stop_client,
                'status': self._show_client_status
            }
        }
        self._help_msg = HELP_MSG
        '''
        Tornado TCP Server & Client
        '''
        self._server_holder = TornadoTCPServerHolder()
        self._client_holder = TornadoTCPClientHolder()

    def _dispatch(self, cmds, cmd_state):
        """
        dispatch cmds on cmd state machine
        :param cmds: cmd.split(' ')
        :param cmd_state: the current state of cmd
        :return:
        """
        len_cmd = len(cmds)
        if len_cmd == 0 or cmds[0] not in cmd_state.keys():
            return False
        state = cmd_state[cmds[0]]
        if callable(state):
            sig = signature(state)
            len_pars = len(sig.parameters)
            if len_pars == 0:
                return state() if len_cmd == 1 else False
            else:
                return functools.partial(state, cmds[1:])() if len_cmd > 1 else state()
        else:
            return self._dispatch(cmds[1:], state) if len_cmd > 1 else False

    def _exit(self):
        """
        Exit TornadoCenter
        :return:
        """
        self._log('Exiting TornadoCenter...')
        if self._server_holder.is_server_active():
            self._server_holder.stop()
        Util.suicide()
        return True

    def _help(self):
        """
        Print help message
        """
        self._log(self._help_msg)
        return True

    def _show_server_params(self):
        """
        Show the params of TCPServer
        """
        if not self._server_holder:
            self._exception('TCPServerHolder is not initialized!')
        else:
            params = self._server_holder.get_params()
            self._log(Util.pformat(params))
            return True

    def _show_server_status(self):
        """
        Show the status of TCPServer
        """
        is_active = self._server_holder.is_server_active()
        if is_active:
            self._log('The server is active!')
        else:
            self._log('The server is stopped!')
        return True

    def _show_client_status(self):
        """
        Show the status of TCPClient
        """
        is_active = self._client_holder.is_client_active()
        if is_active:
            self._log('The client is active!')
        else:
            self._log('The client is stopped!')
        return True

    def _start_server(self, cmds=None):
        """
        Start the TCPServer singleton
        """
        # parse cmd argv
        params = dict()
        if cmds:
            try:
                opts, args = getopt.getopt(cmds, 'p:n:')
                for opt, arg in opts:
                    if opt == '-p':
                        params['port'] = arg
                    if opt == '-n':
                        params['num_processes'] = arg
            except getopt.GetoptError:
                self._exception('Invalid command!!!\n\tserver start [-p <port>]')
                return False
        # initialize tornado server
        self._server_holder.set_params(params)
        ret = self._server_holder.start()
        if ret:
            time.sleep(1)
        return True

    def _start_client(self):
        """
        start the TCPClient
        """
        if not self._server_holder.is_server_active():
            self._exception('Cannot start client! Server is not active!')
        else:
            self._client_holder.set_params(self._server_holder.get_params())
            ret = self._client_holder.start()
            if ret:
                time.sleep(1)
        return True

    def _stop_server(self):
        """
        Stop the TCPServer singleton
        """
        self._server_holder.stop()
        return True

    def _stop_client(self):
        """
        stop the TCPClient
        """
        self._client_holder.stop()
        return True
        
    def loop(self):
        """
        Main loop of TornadoCenter
        :return:
        """
        self._log('Start main loop!!!')
        while True:
            cmd = input('\n$ ').strip()
            if len(cmd) == 0:
                continue
            cmds = cmd.split(' ')
            if not self._dispatch(cmds, self._cmd_state):
                self._exception('Invalid command: %s!' % cmd)
                self._help()


if __name__ == '__main__':
    TornadoCenter().loop()
