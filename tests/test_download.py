# -*-- coding:utf-8 -*--
import unittest
import xlwt
import json
import os
from lib.model import ChangB


class TestDownload(unittest.TestCase):

    def test_suffix(self):
        model = ChangB()
        url1 = 'http://wsbanzou.sslmp3img.changba.com/vod1/zrc/c144b22301f081f56a71c285685b37d3.zrc'
        url2 = 'http://wsbanzou.sslmp3img.changba.com/vod1/mp3/3b40d0cee009c666a93cc3338e936b97.mp3'
        url3 = 'http://wsbanzou.sslmp3img.changba.com/vod1/mp3/3b40d0cee009c666a93cc3338e936b97.txt'
        self.assertEqual('zrc', model.get_url_file_suffix(url1))
        self.assertEqual('mp3', model.get_url_file_suffix(url2))
        self.assertEqual('txt', model.get_url_file_suffix(url3))

    def test_xls_write(self):
        filename = os.path.join(os.curdir, '..', 'data/changba.json')
        xls_filename = os.path.join(os.curdir, '..', 'data/new1.xls')
        file_path = os.path.dirname(filename)
        if not os.path.isdir(file_path):
            os.makedirs(file_path)
        with open(filename) as f:
            items = json.load(f)
            f.close()
        if items:
            work_book = xlwt.Workbook()
            ws = work_book.add_sheet('sheet1')
            count = 0
            ws.write(count, 0, u'作者')
            ws.write(count, 1, u'歌名')
            ws.write(count, 2, u'歌词下载')
            ws.write(count, 3, u'原唱')
            ws.write(count, 4, u'伴奏')
            for item in items['result']:
                count += 1
                self.add_item(ws, count, item)
            work_book.save(xls_filename)
        self.assertTrue(True)

    @staticmethod
    def add_item(ws, count, item):
        ws.write(count, 0, item['name'])
        ws.write(count, 1, item['artist'])
        ws.write(count, 2, item['zrc'])
        ws.write(count, 3, item['mp3'])
        ws.write(count, 4, item['original_mp3'])
