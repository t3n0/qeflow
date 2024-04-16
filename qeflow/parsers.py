'''
Module with all the parsers
'''

from qeflow import __version__

import argparse

def getArgs():
    parser = argparse.ArgumentParser(
        prog = 'qeflow',
        description='QE-flow: automating quantum espresso workflows without scassamento di maroni.')
    parser.add_argument("inputFile", help="input file, default is %(default)s", type=str)
    parser.add_argument("-v", "--verbose", help="verbosity level counter, e.g. -vvv = 3", action='count', default=0)
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    return parser.parse_args()
