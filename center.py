import functools
from util import Util


class TornadoCenter:
    """
    Center Handler
    """
    def __init__(self):
        print('Welcome to TornadoCenter!!!')
        self._tag = 'TornadoCenter'
        self._cmd_map = {
            'exit': self._exit,
            'help': self._help
        }
        self._help_msg = 'Valid commands are: \n' \
            '\texit: Exit the TornadoCenter\n' \
            '\thelp: Show this help message'

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

    def _log(self, msg):
        Util.log(self._tag, msg)
        
    def loop(self):
        self._log('Start main loop!!!')
        while True:
            cmd = input('\n$ ')
            if not self._dispatch(cmd):
                Util.exception('Invalid command: %s!' % cmd, self._log)
                self._help()


if __name__ == '__main__':
    TornadoCenter().loop()

