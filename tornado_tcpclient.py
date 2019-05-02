from tornado.tcpclient import TCPClient
from tornado.iostream import StreamClosedError
from util import BaseCSHolder, Logger
from multiprocessing import Process
import json
from tornado import gen
import asyncio


class TornadoTCPClientHolder(BaseCSHolder):
    """
    Tornado TCPClient Holder
    """
    def __init__(self):
        BaseCSHolder.__init__(self, 'TCPClientHolder')
        self._process = None
        self._params = dict()

    def is_client_active(self):
        return self._process and self._process.is_alive()

    def start(self):
        self._log('Starting Tornado TCPClient...')
        if not self._params:
            self._exception('Cannot start client! The parameters are not set!')
            return False
        if self.is_client_active():
            self._exception('Cannot start client! The TCPClient is still active!')
            return False
        self._process = TornadoTCPClientProcess(self._params)
        self._process.start()
        return True

    def stop(self):
        self._log('Stopping Tornado TCPClient...')
        if self.is_client_active():
            self._process.terminate()
            self._process.join(5)
            return True
        else:
            self._exception('The TCPClient has already been stopped!')
            return False


class TornadoTCPClientProcess(Process, Logger):
    """
    Tornado TCPClient Process
    """
    def __init__(self, params):
        Process.__init__(self, daemon=True)
        Logger.__init__(self, 'TCPClientProcess')
        self._params = params
        self._client = TornadoTCPClient()

    def run(self):
        host, port = self._params['host'], self._params['port']
        task = self._client.start(host, port)
        asyncio.run(task)


class TornadoTCPClient(TCPClient, Logger):
    """
    TCPClient instance of tornado
    """
    def __init__(self):
        TCPClient.__init__(self)
        Logger.__init__(self, 'TCPClient')

    async def start(self, host, port):
        stream = await self.connect(host=host, port=port)
        proto_cnt = 0
        while True:
            try:
                proto_cnt += 1
                if proto_cnt % 2 == 0:
                    await stream.write(('STRING|%d' % proto_cnt).encode('utf-8'))
                else:
                    await stream.write(('JSON|%s' % json.dumps({'proto_cnt': proto_cnt})).encode('utf-8'))
                await gen.sleep(5)
            except StreamClosedError:
                self._log('Client connected to %s:%s is closed!' % (host, port))
                break
