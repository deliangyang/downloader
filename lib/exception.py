# -*-- coding:utf-8 -*--


class HttpNotFound(Exception):
    """http status code 404 not found"""
    def __init__(self):
        message = '下载失败'
        Exception.__init__(self, message)


class UnValidUrl(Exception):
    """un valid url"""
    def __init__(self):
        message = '无效url'
        Exception.__init__(self, message)
