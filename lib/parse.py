# -*-- coding:utf-8 -*--
import xlrd
import logging
from lib.model import ChangB


class Reader(object):

    def __init__(self, filename):
        self.filename = filename

    def read(self):
        sheet = xlrd.open_workbook(filename=self.filename)
        table = sheet.sheet_by_index(0)
        logging.info('read success:%s' % self.filename)
        for row in range(1, table.nrows):
            item = table.row_values(row)
            cb = ChangB()
            cb.song = item[0]
            cb.artist = item[1]
            cb.lyric = item[2]
            cb.audio = item[3]
            cb.origin = item[4]
            yield cb
