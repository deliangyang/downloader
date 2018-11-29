# -*-- coding:utf-8 -*--
import unittest
import os
from lib.parse import Reader


class TestReader(unittest.TestCase):

    def test_read_data(self):
        filename = os.path.join(os.curdir, '..', 'data/1542360094.95.xlsx')
        reader = Reader(filename)
        reader.read()

