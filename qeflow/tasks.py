
from qeflow.logger import Logger
from qeflow.pwx import createPwx


def createTask(task, logger = Logger()):
    if task['task'] in ['vc-relax', 'scf', 'nscf', 'bands']:
        logger.info(f'   {task['task']} input file:\n   {task['fileNameIn']}', 2)
        createPwx(task)


def runTask(task, logger = Logger()):
    if task['task'] in ['vc-relax', 'scf', 'nscf', 'bands']:
        pass

def parseTask(task, logger = Logger()):
    pass

    
