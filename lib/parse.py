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
            ChangB.song = item[0]
            ChangB.artist = item[1]
            ChangB.lyric = item[2]
            ChangB.audio = item[3]
            ChangB.origin = item[4]
            yield ChangB
