import sys
import traceback


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
