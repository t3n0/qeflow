
from qeflow.logger import Logger
from qeflow.utils import runProcess
from qeflow.pwx import createPwx, parsePwx
import os


def createTask(task, logger = Logger()):
    if task['task'] in ['vc-relax', 'scf', 'nscf', 'bands']:
        logger.info(f'   {task["task"]} input file:\n   {task["fileNameIn"]}', 2)
        createPwx(task)


def runTask(task, logger = Logger()):
    logger.info(f'   Running task {task["task"]}...', 1, end='')
    process = runProcess(task['command'], task['fileNameIn'], task['fileNameOut'])
    if process.returncode == 0:
        logger.info(f' success.', 1)
    else:
        logger.info(f'\n   Task {task["task"]} exited with status: {process.returncode}')
        raise Exception('FailedTaskError')


def parseTask(task, logger = Logger()):
    if task['task'] in ['vc-relax', 'scf', 'nscf', 'bands']:
        parsePwx(task)

    

    
