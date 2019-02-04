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
