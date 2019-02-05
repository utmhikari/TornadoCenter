import functools
import time
import getopt
from inspect import signature
from util import Util, Logger
from tornado_tcpserver import TornadoTCPServerHolder
from tornado_tcpclient import TornadoTCPClientHolder


class TornadoCenter(Logger):
    """
    Center Handler
    """
    def __init__(self):
        """
        Initialization
        """
        super().__init__()
        self._log('Welcome to TornadoCenter!!!')
        self._tag = 'TornadoCenter'
        self._cmd_state = {
            'exit': self._exit,
            'help': self._help,
            'server': {
                'start': self._start_server,
                'stop': self._stop_server,
                'params': self._show_server_params,
            }
        }
        self._help_msg = 'Valid commands are: \n' \
                         '\texit: Exit the TornadoCenter\n' \
                         '\thelp: Show this help message'
        '''
        Tornado TCP Server & Client
        '''
        self._server_holder = None
        self._client_holder = None

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
        Util.suicide()
        return True

    def _help(self):
        """
        Print help message
        :return:
        """
        self._log(self._help_msg)
        return True

    def _show_server_params(self):
        """
        Show the params of TCPServer
        :return:
        """
        if not self._server_holder:
            self._exception('TCPServerHolder is not initialized!')
            return False
        params = self._server_holder.get_params()
        self._log(Util.pformat(params))
        return True

    def _start_server(self, cmds=None):
        """
        Start the TCPServer singleton
        :return:
        """
        # parse cmd argv
        params = dict()
        if cmds:
            try:
                opts, args = getopt.getopt(cmds, 'p:')
                for opt, arg in opts:
                    if opt == '-p':
                        params['port'] = arg
            except getopt.GetoptError:
                self._exception('Invalid command!!!\n\tserver start [-p <port>]')
                return False
        # initialize tornado server
        self._server_holder = TornadoTCPServerHolder()
        self._server_holder.set_params(params)
        self._server_holder.start()
        time.sleep(1)
        return True

    def _stop_server(self):
        """
        Stop the TCPServer singleton
        :return:
        """
        self._log('Stopping Tornado TCPServer')
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
