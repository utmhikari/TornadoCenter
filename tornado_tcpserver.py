from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado import ioloop
from util import BaseCSHolder, Logger
from multiprocessing import Process, Queue
from threading import Thread
import json
import time


class TornadoTCPServerHolder(BaseCSHolder):
    """
    Tornado TCPServer Holder
    """
    def __init__(self):
        """
        Initialization
        """
        BaseCSHolder.__init__(self, 'TCPServerHolder')
        '''
        Server Info
        '''
        self._process = None
        self._queue = Queue()
        self._params = {
            'host': '127.0.0.1',
            'port': 5000,
            'num_processes': 1
        }
        '''
        Monitor Thread
        '''
        self._monitor = None
        self._is_monitor_stop = False

    def _clear_queue(self):
        """
        clear the data in the queue
        :return: is the operation processed?
        """
        if self.is_server_active():
            self._exception('The TCPServer instance is running!')
            return False
        while not self._queue.empty():
            self._queue.get()
        return True

    def _monitor_loop(self):
        """
        Monitor thread, print the data received by the server
        """
        self._log('Starting Monitor...')
        while True:
            if self._is_monitor_stop:
                self._is_monitor_stop = False
                break
            while not self._queue.empty():
                data = self._queue.get()
                try:
                    if data.startswith('JSON|'):
                        json_data = json.loads(data[5:])
                        self._log('Received JSON data: %s\n%s' % (
                            type(json_data), json.dumps(json_data, indent=2)
                        ))
                    else:
                        self._log('Received String: %s' % data)
                except Exception as e:
                    self._exception(e)
            time.sleep(1)

    def _stop_monitor(self):
        """
        stop the monitor
        """
        self._clear_queue()
        if self.is_monitor_active():
            self._is_monitor_stop = True
            self._monitor.join(5)
            self._monitor = None

    def _stop_server(self):
        """
        stop the process
        """
        self._process.terminate()
        self._process.join(5)
        exitcode = self._process.exitcode
        self._log('TCPServer is stopped with exit code %s' % exitcode)

    def get_instance(self):
        """
        get the singleton process of tornado tcp server
        :return: tornado tcp server instance
        """
        if not self.is_server_active():
            self._log('The TCPServer instance is not running!')
        return self._process

    def get_port(self):
        """
        get the port of TCPServer
        :return: port
        """
        return self._params['port']

    def is_monitor_active(self):
        """
        check if the monitor is active
        """
        return self._monitor and self._monitor.is_alive()

    def is_server_active(self):
        """
        check if the TCPServer is active
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
            self._stop_monitor()
            self._process = TornadoTCPServerProcess(queue=self._queue, params=self._params)
            self._process.start()
            self._monitor = Thread(target=self._monitor_loop)
            self._monitor.start()
            return True

    def stop(self):
        """
        Stop Tornado TCPServer Process
        :return:
        """
        self._log('Stopping Tornado TCPServer...')
        if self.is_server_active():
            self._stop_server()
            self._stop_monitor()
            return True
        else:
            self._exception('The TCPServer has already been stopped!')
            return False


class TornadoTCPServerProcess(Process, Logger):
    """
    TCPServer Process
    """
    def __init__(self, queue=None, params=None):
        Process.__init__(self, daemon=True)
        Logger.__init__(self, 'TCPServerProcess')
        self._queue = queue
        self._params = params
        self._server = None

    def run(self):
        """
        run the server
        :return:
        """
        try:
            port, num_processes = map(
                lambda k: self._params[k],
                ['port', 'num_processes']
            )
            self._server = TornadoTCPServer(self._queue)
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
    def __init__(self, queue=None):
        TCPServer.__init__(self)
        Logger.__init__(self, 'TCPServer')
        self._queue = queue

    async def handle_stream(self, stream, address):
        host, port = address
        addr = '%s:%s' % (host, port)
        self._log('Handling stream at %s' % addr)
        proto_cnt = 0
        await stream.write('Welcome to tornado server!'.encode('utf-8'))
        while True:
            try:
                data = await stream.read_bytes(4096, partial=True)
                decode_data = data.decode().strip()
                self._queue.put(decode_data)
                proto_cnt += 1
                if proto_cnt % 10 == 0:
                    self._log('Received %d protos from %s!' % (proto_cnt, addr))
            except StreamClosedError:
                self._log('Stream at %s:%s is closed!' % (host, port))
                break
