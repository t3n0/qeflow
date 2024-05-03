
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
    with open(path, 'w') as wf:
            dump(data, wf)


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


