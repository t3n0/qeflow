'''
Simple logging and printing function
'''


from functools import partial
from io import StringIO


print_f = partial(print, flush=True)


class Logger(object):
    def __init__(self, verbose = 0) -> None:
        self.verbose = verbose
        self.log = StringIO()

    # verbose print and logging
    def info(self, text, verbosity = 0, **kwargs):
        if verbosity <= self.verbose:
            print_f(text, **kwargs)
        print(text, file=self.log, **kwargs)

    def getLog(self):
        contents = self.log.getvalue()
        self.log.close()
        return contents