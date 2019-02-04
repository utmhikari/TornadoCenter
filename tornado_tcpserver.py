from tornado.tcpserver import TCPServer
from util import Logger
from multiprocessing import Process


class TornadoTCPServerHolder(Process, Logger):
    """
    Tornado TCPServer Holder
    """
    def __init__(self):
        Process.__init__(self, daemon=True)
        self._tag = 'TCPServerHolder'
        self._server = None

    def get_instance(self):
        """
        get the singleton of tornado tcp server
        :return: tornado tcp server instance
        """
        if not self._server:
            self._exception('No instance initialized!')
        return self._server


class TornadoTCPServer(TCPServer, Logger):
    """
    TCPServer instance of tornado
    """
    def __init__(self, args=None):
        self._tag = 'TCPServer'
        TCPServer.__init__(self)

    def handle_stream(self, stream, address):
        self._log('Handling iostream at %s' % address)
