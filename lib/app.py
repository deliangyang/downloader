# -*-- coding:utf-8 -*--
from lib.parse import Reader
from lib.download import Download
import itertools
import logging
import xlwt
import threading
import time
import os


class Application(object):

    def __init__(self, args):
        self.args = args
        if self.args.debug:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def run(self):
        reader = Reader(self.args.file)
        wb = xlwt.Workbook()
        ws = wb.add_sheet(u'下载结果')
        line_count = 0
        mutex = threading.Lock()

        threads = []
        for i in range(self.args.thread):
            iterator = itertools.islice(reader.read(), i, None, self.args.thread)
            thread = Download(iterator, ws, line_count + i, mutex)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
        wb_filename = time.strftime('%Y%m%d-%H-%M-%S', time.localtime(time.time())) + '.xls'
        wb_filename = os.path.join(os.path.curdir, 'data/export', wb_filename)
        wb.save(wb_filename)
        # os.system('start explorer %s' % os.path.join(os.path.curdir, 'data/export', wb_filename))

    @staticmethod
    def grouper(n, iterable):
        it = iter(iterable)
        while True:
            chunk = tuple(itertools.islice(it, n))
            if not chunk:
                return
            yield chunk
