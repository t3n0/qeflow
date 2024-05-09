'''
qeflow main file for entry scripts
'''


from qeflow import __version__
from qeflow.parsers import getArgsQeflow, getArgsQetask, getArgsQeparse


def qeflow():
    args = getArgsQeflow()
    DRY = args.dry
    INPUTPATH = args.inputFile
    VERBOSE = args.verbose
    print(DRY, INPUTPATH, VERBOSE)


def qetask():
    args = getArgsQetask()
    INPUTPATH = args.workflowFile
    I = args.i
    J = args.j
    print(INPUTPATH, I, J)


def qeparse():
    args = getArgsQeparse()
    INPUTPATH = args.workflowFile
    I = args.i
    J = args.j
    print(INPUTPATH, I, J)
