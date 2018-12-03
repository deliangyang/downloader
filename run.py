# -*-- coding:utf-8 -*--
import argparse
import sys
from lib.app import Application


def usage():
    parse = argparse.ArgumentParser()
    parse.add_argument('file', type=str, default=None, help='the file of excel')
    parse.add_argument('--thread', type=int, default=3, help='the number of thread')
    parse.add_argument('--debug', type=bool, default=True, help='set debug model')
    return parse.parse_args(sys.argv[1:])


if __name__ == '__main__':
    arg = usage()
    app = Application(arg)
    app.run()
