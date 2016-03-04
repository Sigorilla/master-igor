import json


class Config(object):
    def __init__(self, file='config.json'):
        """
        Constructor
        :param file: Configuration
        :return:
        """
        self._dictionary = json.load(open(file))

    def get(self, key, default=''):
        """
        Get parameter from config.json
        :param key:
        :param default: Default value
        :return:
        """
        print self._dictionary
        return self._dictionary.get(key, default)
