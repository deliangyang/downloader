# -*-- coding:utf-8 -*--
import threading
import requests
import logging
import hashlib
import os
import time
from lib.model import ChangB
from lib.decrypt import ChangBaDecrypt
from lib.exception import HttpNotFound, UnValidUrl


class Download(threading.Thread):
    def __init__(self, iterator, ws, line_count, mutex):
        threading.Thread.__init__(self)
        self.iterator = iterator
        self.ws = ws
        self.line_count = line_count
        self.mutex = mutex
        self.decrypt = ChangBaDecrypt()

    def run(self):
        logging.info("%s is running..." % self.getName())
        for item in self.iterator:
            # 处理歌词
            suffix = item.get_url_file_suffix(item.lyric)
            filename = 'data/zrc/' + self.get_url_md5(item.lyric) + '.' + suffix
            filename, content = self.storage(item.lyric, filename)

            if suffix and item.lyric:
                if filename and (suffix == 'zrce' or suffix == 'zrc'):
                    decrypted = self.decrypt.decrypt_by_file(filename)
                    logging.info('decrypt zrc file, %s', decrypted and True)
                    if decrypted:
                        decrypted = self.decrypt.convert_to_new(decrypted)
                        result, _filename = self.storage_decrypt_lyric(item.lyric, decrypted.encode('utf-8'))
                        if result:
                            item.zrc = 'data/lyric/' + _filename
                item.lyric = filename

            # 处理原唱
            suffix = item.get_url_file_suffix(item.origin)
            if suffix and item.origin:
                filename = 'data/origin/' + self.get_url_md5(item.origin) + '.' + suffix
                filename, _ = self.storage(item.origin, filename)
                item.origin = filename

            # 处理音频
            suffix = item.get_url_file_suffix(item.audio)
            if suffix and item.audio:
                filename = 'data/audio/' + self.get_url_md5(item.audio) + '.' + suffix
                filename, _ = self.storage(item.audio, filename)
                item.audio = filename
            self.add_items(item)
            logging.info('next')

    def add_items(self, result):
        if self.mutex.acquire():
            try:
                self.ws.write(self.line_count, 0, result.song)
                self.ws.write(self.line_count, 1, result.artist)
                self.ws.write(self.line_count, 2, result.lyric)
                self.ws.write(self.line_count, 3, result.zrc)
                self.ws.write(self.line_count, 4, result.origin)
                self.ws.write(self.line_count, 5, result.audio)
            except Exception as e:
                logging.info('ws write e: %s' % e)
            self.line_count += 3
            logging.info('current line: %d' % self.line_count)
            self.mutex.release()

    @staticmethod
    def storage(url, filename):
        try:
            if len(url) == 0:
                raise UnValidUrl()
            req = requests.get(url)
            logging.info('download %s => %d' % (url, req.status_code))
            if req.status_code != 200:
                raise HttpNotFound()
            data = req.content
            logging.info("download url %s" % url)
            with open(filename, 'wb') as f:
                f.write(data)
                f.close()
            time.sleep(1)
            return filename, data
        except HttpNotFound as e:
            logging.info('download fail %s' % e)
        except Exception as e:
            logging.info('download fail %s' % e)
        return False, None

    @staticmethod
    def check(url, type, suffix):
        types = ChangB.get_types()
        filename = hashlib.md5(url.encode("utf-8")).hexdigest() + '.' + suffix
        filename = os.path.abspath(os.path.join('data', types[type], filename))
        if not os.path.isfile(filename):
            return filename
        return False

    @staticmethod
    def storage_decrypt_lyric(url, content):
        _filename = hashlib.md5(url.encode("utf-8")).hexdigest() + '.txt'
        filename = os.path.abspath(os.path.join('data', 'zrc', _filename))
        with open(filename, 'wb') as f:
            f.write(content)
            f.close()
            return True, _filename
        return False, None

    @staticmethod
    def get_url_md5(url):
        md5 = hashlib.md5(url.encode("utf-8"))
        return md5.hexdigest()
