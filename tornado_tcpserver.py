from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado import ioloop
from util import Logger
from multiprocessing import Process


class TornadoTCPServerHolder(Process, Logger):
    """
    Tornado TCPServer Holder
    """
    def __init__(self):
        """
        Initialization
        """
        Process.__init__(self, daemon=True)
        self._tag = 'TCPServerHolder'
        '''
        Server Info
        '''
        self._server = None
        self._params = {
            'host': '127.0.0.1',
            'port': 5000,
            'num_processes': 1
        }

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

    def get_instance(self):
        """
        get the singleton of tornado tcp server
        :return: tornado tcp server instance
        """
        if not self._server:
            self._log('No instance initialized!')
        return self._server

    def get_param_keys(self):
        """
        get the keys of params
        :return: sorted param keys
        """
        return sorted(self._params.keys())

    def get_params(self):
        """
        get the params
        :return: params dict
        """
        return self._params

    def set_params(self, params):
        """
        set the params of the server
        :return:
        """
        self._log('Setting params of TCPServer...')
        if not isinstance(params, dict):
            self._exception('The argument params must be a dict!')
            return
        for k in params.keys():
            if k in self._params.keys():
                par_type = type(self._params[k])
                # check int
                if par_type == int:
                    if not str.isdigit(params[k]):
                        self._exception('The param %s should be an integer!' % k)
                        continue
                    params[k] = int(params[k])
                # check type of instance at last
                if not type(params[k]) == par_type:
                    self._exception('The param %s does not match the correct data type %s!' %
                                    (k, par_type))
                    continue
                self._params[k] = params[k]
                self._log('Set param %s to %s!' % (k, params[k]))
        self._log('Finished setting params of TCPServer!')


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
