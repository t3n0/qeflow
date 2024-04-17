from qeflow.constants import CWD
from qeflow.logger import Logger
from yaml import safe_load
import os


class InputFile(object):
    def __init__(self, logger = Logger()) -> None:
        self.logger = logger

    def load(self, path):
        self.path = path
        inp = readYaml(self.path, self.logger)
        inp = checkInput(inp, self.logger)
        self.taskDicts = createTasks(inp, self.logger)
        self.inp = inp        
    
    def get(self, key):
        return self.inp[key]
    

def readYaml(path, logger = Logger()):
    '''
    Reads and returns the YAML dictionary.
    '''
    logger.info(f'Reading {path} yaml input file.', 1)
    with open(path,'r') as f: 
        data = safe_load(f)
    return data


def checkInput(inp, logger = Logger()):
    '''
    Basic checks on the yaml input dictionary
    '''

    # checking for wrong input flags
    wrongKeys = [key for key in inp.keys() if key not in _correctKeys]
    logger.info(f'Checking for wrong input flags.', 1)
    if len(wrongKeys)>0:
        for wrongKey in wrongKeys:
            logger.info(f' * Error: `{wrongKey}` flag not recognised.')
        raise Exception('WrongKeyError')

    # removing empty flags
    logger.info(f'Removing empty flags from input.', 1)
    keys = list(inp.keys()) # we need this so python does not complain about size change
    for key in keys:
        if inp[key] == None:
            logger.info(f' * {key} deleted.', 2)
            del inp[key]

    # workflow checks
    logger.info(f'Checking for wrong workflow flags.', 1)

    # check whether workflow is a list
    if type(inp['workflow']) != list:
        logger.info(f' * Error: the workflow flag must be a `list` of tasks.')
        logger.info(f'   Maybe you forgot a dash, - (surrounded by spaces)')
        raise Exception('WrongKeyError')

    # convert workflow entries to empty dict if not defined
    for i, work in enumerate(inp['workflow']):
        if type(work) == str:
            inp['workflow'][i] = {work: {}}
        elif type(work) == dict and None in work.values():
            key = list(work.keys())[0]
            inp['workflow'][i] = {key: {}}

    # checking for wrong workflow flags
    tasks = []
    for work in inp['workflow']:
        tasks.append(list(work.keys())[0]) # append the *only* key of every work
    # tasks is now something like [relax, scf, bands]
    wrongKeys = [key for key in tasks if key not in _correctWorkflow]
    if len(wrongKeys)>0:
        for wrongKey in wrongKeys:
            logger.info(f' * Error: `{wrongKey}` workflow task not recognised.')
        raise Exception('WrongKeyError')
    
    # we make a new entry for the actual tasks
    # e.g. inp['tasks'] = [relax, scf, bands]
    inp['tasks'] = tasks

    # checking withrespectto flag
    if 'withrespectto' in list(inp.keys()):
        pass

    # set default keys
    inp = _defaultKeys | inp

    # reformat paths to absolute paths
    inp['name'] = os.path.abspath(os.path.join(CWD, inp['name']))
    return inp


def createTasks(inp, logger = Logger()):
    taskDicts = []
    # merging dictionary default | explicit, explicit keys overwrite the default ones
    logger.info(f'Defining the workflow.', 1)
    for i, (work, task) in enumerate(zip(inp['workflow'], inp['tasks'])):
        logger.info(f' * task {i:2d}: {task}', 2)
        aux = inp | work[task]
        taskDicts.append(aux)
    return taskDicts


_correctKeys = [
'workflow',
'withrespectto',
'name',
'cluster',
'nprocs',
'pseudo_pots',
'atoms',
'masses',
'positions',
'unit_cell',
'kpoints',
'nbnd',
'prefix',
'pseudo_dir',
'ecutwfc',
'assume_isolated',
'conv_thr',
'mixing_beta',
'restart',]


_correctWorkflow = [
    'relax',
    'scf',
    'nscf',
    'bands',
    'dos',]


_defaultKeys = {
    'name' : os.path.join(CWD, 'pollo'),
    'cluster' : 'local',
    'nprocs' : 1,}
