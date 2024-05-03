from qeflow.constants import CWD
from qeflow.logger import Logger
from qeflow.utils import readYaml
import os


def readInput(path, logger = Logger()):
    logger.info(f'\n--------------------------------', 1)
    logger.info(f'Reading input file from:\n   {path}', 1)
    inp = readYaml(path)
    inp = checkInput(inp, logger)
    return inp


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

    # checking withrespectto flag
    if 'withrespectto' in inp.keys():
        if type(inp['withrespectto']) != list:
            logger.info(f' * Error: `withrespectto` must be a list of dictionaries.')
            raise Exception('WrongKeyError')

    # set default keys
    inp = _defaultKeys | inp

    # reformat paths to absolute paths
    inp['name'] = os.path.abspath(os.path.join(CWD, inp['name']))

    # at last, we define some new entries
    inp['tasks'] = tasks           # e.g. inp['tasks'] = [relax, scf, bands]
    inp['calc_dir'] = os.path.abspath(os.path.join(inp['name'], 'calc'))
    inp['res_dir'] = os.path.abspath(os.path.join(inp['name'], 'results'))
    inp['logger_path'] = os.path.abspath(os.path.join(inp['name'], 'log.txt'))
    inp['workflow_path'] = os.path.abspath(os.path.join(inp['name'], 'workflow.txt'))
    return inp





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
    'w90',
    'w90pp',
    'pw2w90',]


_defaultKeys = {
    'name' : os.path.join(CWD, 'myflow'),
    'nprocs' : 1,
    'time' : '0:20:0',
    'partition' : 'standard',
    'qos' : 'short',
    'withrespectto' : [],}

