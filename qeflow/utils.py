
from subprocess import run, PIPE
from yaml import safe_load, dump
import os
from qeflow.logger import Logger
from qeflow.pwx import Pwx

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

def removeFile(name):
    if os.path.exists(name):
        os.remove(name)


def runProcess(command, inputFile):
    with open(inputFile, 'r') as inp:
        process = run(command.split(), stdin=inp, stdout=PIPE, stderr=PIPE, shell=False, text=True)
        #process = run(command.split(), stdin=inp, shell=False, text=True)
    return process


def runWork(work, logger = Logger()):
    tasks = work['tasks']
    for task in tasks:
        if task['task'] in ['vc-relax', 'scf', 'nscf', 'bands']:
            logger.info(f'Running task {task['task']} on pw.x', 1)
            runner = Pwx(task)
        elif task['task'] in ['w90', 'w90pp']:
            logger.info(f'Running task {task['task']} on wannier90.x', 1)

    


def appendResults(task):
    pass