
from subprocess import run, PIPE
from yaml import safe_load, dump
import os
from qeflow.logger import Logger


def readYaml(path):
    '''
    Reads and returns the YAML dictionary.
    '''
    with open(path,'r') as f: 
        data = safe_load(f)
    return data


def saveYaml(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True) # creates the necessary folders
    with open(path, 'w') as wf:
            dump(data, wf)


def saveFile(data, path, mode='w'):
    os.makedirs(os.path.dirname(path), exist_ok=True) # creates the necessary folders
    with open(path, mode) as f:
        f.write(data)


def createDir(dir, logger = Logger()):
    '''
    Creates a folder if it does not exist already.
    '''
    logger.info(f"Creating new directory:\n   {dir}", 1)
    if not os.path.exists(dir):
        os.makedirs(dir)
        logger.info(f" * directory created successfully.", 2)
    else:
        logger.info(f" * directory already exists.", 2)

def removeFile(name):
    if os.path.exists(name):
        os.remove(name)


def runProcess(command, inputFile, outputFile=None):
    if outputFile == None:
        with open(inputFile, 'r') as inp:
            process = run(command.split(), stdin=inp, stdout=PIPE, stderr=PIPE, shell=False, text=True)
    else:
        with open(inputFile, 'r') as inp, open(outputFile, 'w') as out:
            process = run(command.split(), stdin=inp, stdout=out, stderr=PIPE, shell=False, text=True)
        #process = run(command.split(), stdin=inp, shell=False, text=True)
    return process
