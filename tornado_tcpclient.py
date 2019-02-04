from tornado.tcpclient import TCPClient
from util import Util


class TornadoTCPClient(TCPClient):
    """
    TCPClient instance of tornado
    """
    def __init__(self):
        self._tag = 'TCPClient'
        TCPClient.__init__(self)

    def _log(self, msg):
        Util.log(self._tag, msg)



