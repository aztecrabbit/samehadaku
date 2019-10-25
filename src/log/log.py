import sys
import datetime
from ..utils.utils import utils

class log(object):
    def __init__(self):
        super(log, self).__init__()

        self.utils = utils(__file__)
        self.lock = self.utils.lock

        self.patterns = {
            'CC' : '\033[0m',    'BB' : '\033[1m',
            'D1' : '\033[30;1m', 'D2' : '\033[30;2m',
            'R1' : '\033[31;1m', 'R2' : '\033[31;2m',
            'G1' : '\033[32;1m', 'G2' : '\033[32;2m',
            'Y1' : '\033[33;1m', 'Y2' : '\033[33;2m',
            'B1' : '\033[34;1m', 'B2' : '\033[34;2m',
            'P1' : '\033[35;1m', 'P2' : '\033[35;2m',
            'C1' : '\033[36;1m', 'C2' : '\033[36;2m',
            'W1' : '\033[37;1m', 'W2' : '\033[37;2m',
        }

        self.type = 1
        self.spaces = ' ' * 8
        self.prefix = ''
        self.suffix = ''
        self.value_prefix = ''
        self.value_suffix = ''

    def eval(self, value, color):
        return eval(value).replace('{color}', color).replace('{clear}', '[CC]') + ' ' if value else ''

    def get_value_prefix(self, color):
        return self.eval(self.value_prefix, color)

    def get_value_suffix(self, color):
        return self.eval(self.value_suffix, color)

    def log(self, value, prefix='', suffix='', color='', type=''):
        type = type if type != '' else self.type

        if self.type < type:
            return

        prefix = str(prefix if prefix else self.prefix)
        suffix = str(suffix if suffix else self.suffix)

        value = f"{color}{self.get_value_prefix(color).replace('{prefix}', prefix)}{color}{value}{color}{self.get_value_suffix(color).replace('{suffix}', suffix)}[CC]{self.spaces}"
        with self.lock:
            print(self.utils.colors(value, self.patterns))

    def log_replace(self, value, color='[G1]'):
        with self.lock:
            sys.stdout.write(self.utils.colors(f'{color}{value}[CC]{self.spaces}{self.spaces}\r', self.patterns))
            sys.stdout.flush()

    def keyboard_interrupt(self):
        sys.stdout.write(f'{self.spaces}\r')
        sys.stdout.flush()
        self.log(f'Keyboard interrupted {self.spaces} {self.spaces}       \n\n|   Ctrl-C again if not exiting automaticly \n|   Please wait... \n| \n', color='[R1]', type=0)
