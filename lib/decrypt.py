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
        content = re.sub(r'\[[^\]]+\]\r?\n', '', content)
        lines = re.split(r'\r?\n', content)

        offset_item = re.findall(r'\[(\d+).(\d+)\]', content)
        start, _ = offset_item[0]
        replace_pattern = re.compile(r'(\[\d+,\d+\])')
        main_content = []
        for line in lines:
            if not line.endswith(']') and len(line) > 0:
                line = replace_pattern.sub(r'\1{red}', line)
                main_content.append(line + ';')
        content = '[offset:%d]\n[refrain:%d]\n[halfSong:%d]%s%s' % (
            int(start), 0, 0, "\n" * 6, "\n".join(main_content)
        )
        content.strip('\n')
        return content
