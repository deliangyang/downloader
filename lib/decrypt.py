# -*-- coding:utf-8 -*--
import re


class ChangBaDecrypt(object):
    encrypt_key = [-50, -45, 110, 105, 64, 90, 97, 119, 94, 50, 116, 71, 81, 54, -91, -68, ]

    def __init__(self):
        self.pattern = re.compile(r',0>')

    def decrypt(self, content):
        decrypt_content = bytearray()
        for i in range(0, len(content)):
            var = content[i] ^ self.encrypt_key[i % 16]
            decrypt_content.append(var & 0xff)
        return decrypt_content.decode('utf-8')

    def decrypt_by_file(self, filename):
        with open(filename, 'rb') as f:
            content = f.read()
            f.close()
            decrypt = self.decrypt(content)
            return decrypt

    def convert_to_new(self, content):
        content = self.pattern.sub('>', content)
        return content
