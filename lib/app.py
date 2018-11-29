# -*-- coding:utf-8 -*--
from lib.parse import Reader
from lib.download import Download
import itertools
import logging


class Application(object):

    def __init__(self, args):
        self.args = args
        print(self.args)
        if self.args.debug == 'True':
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def run(self):
        reader = Reader(self.args.file)
        for i in range(self.args.thread):
            thread = Download(itertools.islice(reader.read(), i, None, self.args.thread))
            thread.start()

    @staticmethod
    def grouper(n, iterable):
        it = iter(iterable)
        while True:
            chunk = tuple(itertools.islice(it, n))
            if not chunk:
                return
            yield chunk
