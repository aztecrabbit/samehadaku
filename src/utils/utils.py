import os
from threading import RLock

lock = RLock()

class utils(object):
    def __init__(self, file_path):
        super(utils, self).__init__()

        self.file_path = file_path
        self.lock = lock

    def real_path(self, file_name):
        return os.path.dirname(os.path.abspath(self.file_path)) + file_name

    def colors(self, value='', patterns=''):
        if not patterns:
            patterns = {
                'R1' : '\033[31;1m', 'G1' : '\033[32;1m',
                'Y1' : '\033[33;1m', 'P1' : '\033[35;1m',
                'CC' : '\033[0m'
            }

        for code in patterns:
            value = value.replace('[{}]'.format(code), patterns[code])

        return value

    def banner(self, values, color='[G1]'):
        os.system('cls' if os.name == 'nt' else 'clear')
        for value in values:
            print(self.colors(f'{color}{value}'))
        print(self.colors('[CC]'))

    def xfilter(self, data):
        for i in range(len(data)):
            data[i] = data[i].strip()
            if data[i].startswith('#'):
                data[i] = ''

        return [x for x in data if x]
