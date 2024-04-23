from qeflow.constants import CWD
from qeflow.logger import Logger
from qeflow.utils import readYaml, flatTable
import os


class Inputs(object):
    def __init__(self, logger = Logger()) -> None:
        self.logger = logger

    def load(self, path):
        self.path = path
        self.logger.info(f'Reading {path} input file.', 1)
        inp = readYaml(self.path)
        inp = checkInput(inp, self.logger)
        self.taskDicts = createTasks(inp, self.logger)
        self.inp = inp        
    
    def getInput(self, key):
        return self.inp[key]
    
    def getTasks(self):
        return self.taskDicts


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
        del aux['nprocs']
        del aux['time']
        del aux['partition']
        del aux['qos']
        aux['task'] = task
        flowDicts.append(aux)
    
    # merge all dicts together
    logger.info(f'Workflow that will be performed:', 1)
    for task in inp['tasks']:
        logger.info(f' * {task}', 1)
    taskDicts = []
    if len(wrtDicts) == 0:
        taskDicts = flowDicts
    else:
        logger.info(f'Each workflow will iterate {len(wrtDicts)} times.', 1)
        logger.info(f'Iterating parameters:', 1)
        for wrt in wrtDicts:
            logger.info(f' * { wrt }', 1)
            for flow in flowDicts:
                aux = flow | wrt
                taskDicts.append(aux)
    
    for i, task in enumerate(taskDicts):
        task['fileNameIn'] = f'{i:02d}.in'
        task['fileNameOut'] = f'{i:02d}.out'
    
    return taskDicts


_correctKeys = [
'workflow',
'withrespectto',
'name',
'nprocs',
'time',
'partition',
'qos',

'pseudo_pots',
'atoms',
'masses',
'positions',
'unit_cell',

'restart',
'prefix',
'pseudo_dir',
'verbosity',

'kpoints',
'lspinorb',
'noncolin',
'nosym',
'nbnd',
'ecutwfc',
'assume_isolated',
'conv_thr',
'mixing_beta',
'cell_dofree',]


_correctWorkflow = [
    'scf',
    'nscf',
    'bands',
    'relax',
    'vc-relax',
    'dos',
    'w90',]


_defaultKeys = {
    'name' : os.path.join(CWD, 'myflow'),
    'nprocs' : 1,
    'time' : '0:20:0',
    'partition' : 'standard',
    'qos' : 'short',
    'withrespectto' : [],}

