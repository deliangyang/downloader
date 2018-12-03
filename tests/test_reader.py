# -*-- coding:utf-8 -*--
import unittest
import os
from lib.parse import Reader
from lib.decrypt import ChangBaDecrypt
import re


class TestReader(unittest.TestCase):

    def test_read_data(self):
        filename = os.path.join(os.curdir, '..', 'data/1542360094.95.xlsx')
        reader = Reader(filename)
        reader.read()

    def test_decrypt(self):
        changba = ChangBaDecrypt()
        content = changba.decrypt_by_file(os.path.join(os.curdir, '..', 'data/a89f8523a6724a915c6b2038c928b342.zrce'))
        self.assertRegex(content, re.compile(r'<'))
