
from qeflow.logger import Logger
from qeflow.pwx import createPwx


def createTask(task, logger = Logger()):
    if task['task'] in ['vc-relax', 'scf', 'nscf', 'bands']:
        logger.info(f'Running task {task['task']} on pw.x', 1)
        createPwx(task)


def runTask(task):
    pass


def parseTask(task):
    pass

    
