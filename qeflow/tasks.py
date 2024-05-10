
from qeflow.logger import Logger
from qeflow.utils import runProcess
from qeflow.pwx import createPwx


def createTask(task, logger = Logger()):
    if task['task'] in ['vc-relax', 'scf', 'nscf', 'bands']:
        logger.info(f'   {task['task']} input file:\n   {task['fileNameIn']}', 2)
        createPwx(task)


def runTask(task, logger = Logger()):
    logger.info(f'   Running task {task['task']}...', 1, end='')
    runProcess(task['command'], task['fileNameIn'])
    logger.info(f'done.', 1)

def parseTask(task, logger = Logger()):
    pass

    
