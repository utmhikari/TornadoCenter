from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado import ioloop
from util import BaseCSHolder, Logger
from multiprocessing import Process


class TornadoTCPServerHolder(BaseCSHolder):
    """
    Tornado TCPServer Holder
    """
    def __init__(self):
        """
        Initialization
        """
        BaseCSHolder.__init__(self)
        self._tag = 'TCPServerHolder'
        '''
        Server Info
        '''
        self._process = None
        self._params = {
            'host': '127.0.0.1',
            'port': 5000,
            'num_processes': 1
        }

    def get_instance(self):
        """
        get the singleton process of tornado tcp server
        :return: tornado tcp server instance
        """
        if not self.is_server_active():
            self._log('The TCPServer instance is not running!')
        return self._process

    def is_server_active(self):
        """
        check if the TCPServer is active
        :return:
        """
        return self._process and self._process.is_alive()

    def start(self):
        """
        Start Tornado TCPServer Process
        :return:
        """
        self._log('Starting Tornado TCPServer...')
        if self.is_server_active():
            self._exception('Cannot start server! The TCPServer is still active!')
            return False
        else:
            self._process = TornadoTCPServerProcess(self._params)
            self._process.start()
            return True

    def stop(self):
        """
        Stop Tornado TCPServer Process
        :return:
        """
        self._log('Stopping Tornado TCPServer...')
        if self.is_server_active():
            self._process.terminate()
            self._process.join(5)
            exitcode = self._process.exitcode
            if exitcode:
                self._log('TCPServer is stopped with exit code %s' % exitcode)
                self._process = None
                return True
            else:
                self._exception('TCPServer is not yet stopped! Please try again!')
                return False
        else:
            self._exception('The TCPServer has already been stopped!')
            return False


class TornadoTCPServerProcess(Process, Logger):
    """
    TCPServer Process
    """
    def __init__(self, params):
        Process.__init__(self, daemon=True)
        self._tag = 'TCPServerProcess'
        self._params = params
        self._server = None

    def run(self):
        """
        run the server
        :return:
        """
        self._log('Starting TCPServer...')
        try:
            port, num_processes = map(
                lambda k: self._params[k],
                ['port', 'num_processes']
            )
            self._server = TornadoTCPServer()
            self._server.bind(port)
            self._server.start(num_processes)
            self._log('TCPServer started successfully at 127.0.0.1:%s' % port)
            self._log('Starting IOLoop...')
            ioloop.IOLoop().current().start()
        except Exception as e:
            self._exception('Start TCPServer Failed! %s' % e, is_trace=True)


class TornadoTCPServer(TCPServer, Logger):
    """
    TCPServer instance of tornado
    """
    def __init__(self):
        self._tag = 'TCPServer'
        TCPServer.__init__(self)

    async def handle_stream(self, stream, address):
        host, port = address
        self._log('Handling stream at %s:%s' % (host, port))
        while True:
            try:
                data = await stream.read_bytes(4096, partial=True)
                decode_data = data.decode().strip()
                self._log('[%s:%s] Received data: %s' % (host, port, decode_data))
            except StreamClosedError:
                self._log('Stream at %s:%s is closed!' % (host, port))
                break
