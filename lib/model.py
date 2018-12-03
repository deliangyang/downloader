# -*-- coding:utf-8 -*--
import re


class ChangB(object):
    __slots__ = ('song', 'artist', 'lyric', 'origin', 'audio', 'container', 'pattern')

    def __init__(self):
        self.container = {}
        self.pattern = re.compile(r'\.(\w+$)')

    def __setitem__(self, key, value):
        self.container.pop(key, value)

    @staticmethod
    def get_types():
        return ['lyric', 'origin', 'audio']

    def get_url_file_suffix(self, url):
        item = self.pattern.findall(url)
        if item:
            return item[0]
        return False
