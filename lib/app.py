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
        self.add_xls_header(ws)
        line_count = 1
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
        try:
            file_path = os.path.dirname(wb_filename)
            if not os.path.isdir(file_path):
                os.makedirs(file_path)
        except Exception as e:
            logging.info('create dir: %s' % e)
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

    def add_xls_header(self, ws):
        ws.write(0, 0, u'歌名')
        ws.write(0, 1, u'歌唱者')
        # self.ws.write(self.line_count, 2, result.lyric)
        ws.write(0, 2, u'歌词')
        ws.write(0, 3, u'原唱')
        ws.write(0, 4, u'伴奏')
