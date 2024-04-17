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
        return inp
    

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
    userKeys = list(inp.keys())
    wrongKeys = [key for key in userKeys if key not in _correctKeys]
    logger.info(f'Checking for wrong input flags.', 1)
    if len(wrongKeys)>0:
        for wrongKey in wrongKeys:
            logger.info(f' * Error: `{wrongKey}` flag not recognised.')
        raise Exception('WrongKeyError')

    # removing empty flags
    logger.info(f'Removing empty flags from input.', 1)
    keys = list(inp.keys())
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

    # convert workflow entries to dict
    for i, task in enumerate(inp['workflow']):
        if type(task) != dict:
            inp['workflow'][i] = {task: None}

    # checking for wrong workflow flags
    userKeys = []
    for task in inp['workflow']:
        userKeys.append(list(task.keys())[0]) # append the *only* key of every task
    wrongKeys = [key for key in userKeys if key not in _correctWorkflow]
    if len(wrongKeys)>0:
        for wrongKey in wrongKeys:
            logger.info(f' * Error: `{wrongKey}` workflow task not recognised.')
        raise Exception('WrongKeyError')
    
    # checking withrespectto flag
    if 'withrespectto' in list(inp.keys()):
        pass


    return inp


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
    'cluster' : 'local',
    'nprocs' : 1,
    'prefix' : 'pollo',
    'pseudo_dir' : os.path.join(CWD, 'ppdir'),
    'outdir' : os.path.join(CWD, 'calc', 'pollo'),
    'calc_dir' : os.path.join(CWD, 'calc'),
    'res_dir' : os.path.join(CWD, 'results'),
    'ecutwfc' : 50,
    'nosym' : False,
    'assume_isolated' : 'none',
    'conv_thr' : 1e-8,
    'mixing_beta' : 0.7,}