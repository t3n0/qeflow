from qeflow.constants import CWD
from qeflow.logger import Logger
from yaml import safe_load
import os


class Inputs(object):
    def __init__(self, logger = Logger()) -> None:
        self.logger = logger

    def load(self, path):
        self.path = path
        inp = readYaml(self.path, self.logger)
        inp = checkInput(inp, self.logger)
        self.taskDicts = createTasks(inp, self.logger)
        self.inp = inp        
    
    def getInput(self, key):
        return self.inp[key]
    
    def getTasks(self):
        return self.taskDicts
    

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
        tasks.append(list(work.keys())[0]) # append the *only* key of each work
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
    if 'withrespectto' in inp.keys():
        if type(inp['withrespectto']) != list:
            logger.info(f' * Error: `withrespectto` must be a list of dictionaries.')
            raise Exception('WrongKeyError')

    # set default keys
    inp = _defaultKeys | inp

    # reformat paths to absolute paths
    inp['name'] = os.path.abspath(os.path.join(CWD, inp['name']))
    return inp


def createTasks(inp, logger = Logger()):
    '''
    Returns a list of dictionaries. Each dictionary is the input of a specific code in the workflow.
    Also, each dictionary is the cartesian product of the `withrespectto` flag entries.
    '''

    keys = []
    table = []
    for wrt in inp['withrespectto']:
        for k, v in wrt.items():
            keys.append(k)
            table.append(v)
    flat_table = flatTable(table)

    wrtDicts = []
    for values in flat_table:
        aux = {}
        for k,v in zip(keys, values):
            aux[k] = v
        wrtDicts.append(aux)

    # merging dictionary default | explicit, explicit keys overwrite the default ones
    flowDicts = []
    for work, task in zip(inp['workflow'], inp['tasks']):
        aux = inp | work[task]
        del aux['workflow']
        del aux['tasks']
        del aux['withrespectto']
        aux['task'] = task
        flowDicts.append(aux)
    
    # merge all dicts together
    logger.info(f'Workflow that will be performed: {inp['tasks']}', 1)
    taskDicts = []
    if len(wrtDicts) == 0:
        taskDicts = flowDicts
    else:
        logger.info(f'Each workflow will iterate {len(wrtDicts)} times.', 1)
        logger.info(f'Iterating parameters:', 2)
        for wrt in wrtDicts:
            logger.info(f' * { wrt }', 2)
            for flow in flowDicts:
                aux = flow | wrt
                taskDicts.append(aux)
    return taskDicts


def joinList(arr1, arr2):
    '''
    Joins two lists and makes the carteisn product list.
    Example:
    arr1 = [1,2]
    arr2 = [4,5,6]
    arr = [[1, 4], [2, 4], [1, 5], [2, 5], [1, 6], [2, 6]]
    '''
    arr = []
    if len(arr1) == 0:
        arr = arr2
    elif len(arr1) > 0:
        for a2 in arr2:
            if type(a2) != list: a2 = [a2]
            for a1 in arr1:
                if type(a1) != list: a1 = [a1]
                arr.append(a1 + a2)
    return arr


def flatTable(table):
    '''
    Returns the flatten cartesian product of all lists in table.
    Example:
    arr1 = [1,2]
    arr2 = [4,5,6]
    arr3 = ['ciao', 'ciccio']
    table = [arr1, arr2, arr3]
    aux =  [[1, 4, 'ciao'],
            [2, 4, 'ciao'], 
            [1, 5, 'ciao'], 
            [2, 5, 'ciao'], 
            [1, 6, 'ciao'], 
            [2, 6, 'ciao'], 
            [1, 4, 'ciccio'], 
            [2, 4, 'ciccio'], 
            [1, 5, 'ciccio'], 
            [2, 5, 'ciccio'], 
            [1, 6, 'ciccio'], 
            [2, 6, 'ciccio']]
    '''
    if len(table) == 1:
        return [ [a] for a in table[0]]
    else:
        aux = []
        for tab in table:
            aux = joinList(aux, tab)
        return aux


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
    'scf',
    'nscf',
    'bands',
    'relax',
    'vc-relax',
    'dos',
    'w90',]


_defaultKeys = {
    'name' : os.path.join(CWD, 'pollo'),
    'cluster' : 'local',
    'nprocs' : 1,
    'withrespectto' : [],}
