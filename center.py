import functools
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
        self._cmd_map = {
            'exit': self._exit,
            'help': self._help
        }
        self._help_msg = 'Valid commands are: \n' \
                         '\texit: Exit the TornadoCenter\n' \
                         '\thelp: Show this help message'
        self._server_holder = TornadoTCPServerHolder()
        self._client_holder = TornadoTCPClientHolder()

    def _dispatch(self, cmd):
        if cmd not in self._cmd_map.keys():
            return False
        state = self._cmd_map[cmd]
        if callable(state):
            state()
            return True
    
    def _exit(self):
        self._log('Exiting TornadoCenter...')
        Util.suicide()

    def _help(self):
        print(self._help_msg)
        
    def loop(self):
        self._log('Start main loop!!!')
        while True:
            cmd = input('\n$ ')
            if not self._dispatch(cmd):
                self._exception('Invalid command: %s!' % cmd)
                self._help()


if __name__ == '__main__':
    TornadoCenter().loop()
