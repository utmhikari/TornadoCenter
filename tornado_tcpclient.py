from tornado.tcpclient import TCPClient
from util import BaseCSHolder, Logger
from multiprocessing import Process


class TornadoTCPClientHolder(BaseCSHolder):
    """
    Tornado TCPClient Holder
    """
    def __init__(self):
        BaseCSHolder.__init__(self)
        self._tag = 'TCPClientHolder'
        self._clients = dict()
        self._params = dict()


class TornadoTCPClientProcess(Process, Logger):
    """
    Tornado TCPClient Process
    """
    def __init__(self, params):
        Process.__init__(self, daemon=True)
        self._tag = 'TCPClientProcess'


class TornadoTCPClient(TCPClient, Logger):
    """
    TCPClient instance of tornado
    """
    def __init__(self):
        TCPClient.__init__(self)
        self._tag = 'TCPClient'
