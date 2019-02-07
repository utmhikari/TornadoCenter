import sys
import traceback
import pprint


class Util:
    """
    Common Utils
    """
    @staticmethod
    def check_key(dictionary, key, default_value):
        """
        check key of a dict, if no key, create it
        :param dictionary:
        :param key:
        :param default_value:
        :return:
        """
        if type(dictionary) != 'dict':
            return False
        if key not in dictionary.keys():
            dictionary[key] = default_value
            return False
        return True

    @staticmethod
    def exception(err, callback=print, is_trace=False):
        """
        print exception
        """
        callback('Error! %s' % err)
        if is_trace:
            traceback.print_exc()

    @staticmethod
    def log(tag, msg):
        """
        print log
        """
        print('[%s] %s' % (tag, msg))

    @staticmethod
    def pformat(obj):
        """
        format obj to string with indent of 2
        :param obj: obj to be formatted
        :return: formatted string
        """
        return pprint.pformat(obj, indent=2)

    @staticmethod
    def suicide():
        """
        kill self
        """
        sys.exit(0)


class Logger:
    """
    Logger Class
    """
    def __init__(self):
        self._tag = 'Logger'

    def _log(self, msg):
        """
        print log with tag, like log.d in android applications
        """
        Util.log(self._tag, msg)

    def _exception(self, err, is_trace=False):
        """
        print exception with self._log as callback
        """
        Util.exception(err, self._log, is_trace)


class BaseCSHolder(Logger):
    """
    Client and Server Holder Class
    """
    def __init__(self):
        Logger.__init__(self)
        self._params = dict()

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
        self._log('Setting params of %s...' % self._tag)
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
        self._log('Finished setting params of %s!' % self._tag)
