# -*-- coding:utf-8 -*--
import threading
import requests
import logging
import hashlib
import os
import re


class Download(threading.Thread):
    def __init__(self, iterator):
        threading.Thread.__init__(self)
        self.iterator = iterator

    def run(self):
        logging.info("%s is running..." % self.getName())
        for item in self.iterator:
            mp3 = self.check(item.lyric, 1)
            if mp3:
                self.storage(item.lyric, mp3)

    @staticmethod
    def storage(url, filename):
        req = requests.get(url)
        data = req.content
        logging.info("download url %s" % url)
        with open(filename, 'wb') as f:
            f.write(data)
            f.close()

    @staticmethod
    def check(url, type):
        types = ['lyric', 'origin', 'audio']
        filename = hashlib.md5(url.encode("utf-8")).hexdigest() + '.mp3'
        filename = os.path.abspath(os.path.join('data', types[type], filename))
        if not os.path.isfile(filename):
            return filename
        return False
