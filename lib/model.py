# -*-- coding:utf-8 -*--


class ChangB(object):
    __slots__ = ('song', 'artist', 'lyric', 'origin', 'audio')

    def __init__(self):
        self.container = {}

    def __setitem__(self, key, value):
        self.container.pop(key, value)
