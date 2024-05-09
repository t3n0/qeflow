'''
Simple logging and printing function
'''


from functools import partial
import os
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
    
    def saveLog(self, path, mode='w'):
        os.makedirs(os.path.dirname(path), exist_ok=True) # creates the necessary folders
        with open(path, mode) as logfile:
            logfile.write(self.getLog())
        