from qeflow.constants import CWD, HOME
from qeflow.logger import Logger
from qeflow.utils import readYaml
import os


def readConfig(logger = Logger()):
    '''
    Read the configuration file and returns a dictionary.
    First it checks the local folder, then HOME, then default configs are loaded.
    '''
    if os.path.exists(os.path.join(CWD, 'qeflow.cfg')):
        cfgFilePath = os.path.join(CWD, 'qeflow.cfg')
    elif os.path.exists(os.path.join(HOME, '.qeflow.cfg')):
        cfgFilePath = os.path.join(HOME, '.qeflow.cfg')
    else:
        cfgFilePath = None

    if cfgFilePath:
        logger.info(f'\n--------------------------------', 1)
        logger.info(f'Reading configuration file from:\n   {cfgFilePath}', 1)
        configs = readYaml(cfgFilePath)

        # check for wrong config keys
        wrongKeys = [key for key in configs.keys() if key not in correctKeys]
        if len(wrongKeys)>0:
            for wrongKey in wrongKeys:
                logger.info(f' * Error: `{wrongKey}` flag not recognised.')
            raise Exception('WrongKeyError')
        
        # removing empty flags
        logger.info(f'Removing empty flags from config.', 1)
        keys = list(configs.keys()) # we need this so python does not complain about size change
        for key in keys:
            if configs[key] == None:
                logger.info(f' * {key} deleted.', 2)
                del configs[key]
        
        logger.info(f'Set missing configs with default ones.', 1)
        configs = defaultConfigs | configs
    else:
        logger.info(f'Configuration file is absent.', 1)
        logger.info(f' * default configuration will be used', 1)
        configs = defaultConfigs
    
    # definition of all the executables for any given task
    execDict = {
        'scf' : f'{configs["pwx"]}',
        'nscf' : f'{configs["pwx"]}',
        'bands' : f'{configs["bandsx"]}',
        'relax' : f'{configs["pwx"]}',
        'vc-relax' : f'{configs["pwx"]}',
        'md' : f'{configs["pwx"]}',
        'vc-md' : f'{configs["pwx"]}',
        'dos' : f'{configs["dosx"]}',
        'ph' : f'{configs["phx"]}',
        'w90' : f'{configs["w90x"]}',
        'w90pp' : f'{configs["w90x"]} -pp',
        'pw2w90' : f'{configs["pw2w90x"]}',
    }

    # join averything into the configs dictionary
    configs = configs | execDict

    # print configs to logger
    logger.info(f'The system configuration is:', 2)
    for k,v in configs.items():
        logger.info(f' * {k} : {v}', 2)
    return configs
    

correctKeys = {
    'cluster',
    'account',
    'pyenv',
    'modules',
    'cores_per_node',
    'pwx',
    'phx',
    'ppx',
    'dosx',
    'bandsx',
    'projwfcx',
    'plotbandx',
    'w90x',
    'pw2w90x',
    'mpix',
}

defaultConfigs = {
    'cluster' : 'local',
    'pwx' : 'pw.x',
    'phx' : 'ph.x',
    'ppx' : 'pp.x',
    'dosx' : 'dos.x',
    'bandsx' : 'bands.x',
    'projwfcx' : 'projwfc.x',
    'plotbandx' : 'plotband.x',
    'w90x' : 'wannier90.x',
    'pw2w90x' : 'pw2wannier90.x',
    'mpix' : 'mpirun',
}