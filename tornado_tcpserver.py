from tornado.tcpserver import TCPServer
from util import Util


class TornadoTCPServer(TCPServer):
    """
    TCPServer instance of tornado
    """
    def __init__(self):
        self._tag = 'TCPServer'
        TCPServer.__init__(self)

    def _log(self, msg):
        Util.log(self._tag, msg)

    def handle_stream(self, stream, address):
        self._log('Handling iostream at %s' % address)


