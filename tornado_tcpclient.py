from tornado.tcpclient import TCPClient
from util import Logger
from multiprocessing import Process


class TornadoTCPClientHolder(Process, Logger):
    """
    Tornado TCPClinet Holder
    """
    def __init__(self):
        self._tag = 'TCPClientHolder'
        Process.__init__(self, daemon=True)


class TornadoTCPClient(TCPClient, Logger):
    """
    TCPClient instance of tornado
    """
    def __init__(self, params=None):
        self._tag = 'TCPClient'
        TCPClient.__init__(self)
