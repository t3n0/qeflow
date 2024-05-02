from qeflow.constants import CWD, HOME
from qeflow.logger import Logger
from qeflow.utils import readYaml
import os


class Config(object):
    def __init__(self, logger = Logger()) -> None:
        self.logger = logger
        
        if os.path.exists(os.path.join(CWD, 'qeflow.cfg')):
            cfgFilePath = os.path.join(CWD, 'qeflow.cfg')
        elif os.path.exists(os.path.join(HOME, '.qeflow.cfg')):
            cfgFilePath = os.path.join(HOME, '.qeflow.cfg')
        else:
            cfgFilePath = None
        
        if cfgFilePath:
            self.logger.info(f'Reading configuration file from:\n   {cfgFilePath}', 1)
            configs = readYaml(cfgFilePath)

            # check for wrong config keys
            wrongKeys = [key for key in configs.keys() if key not in _correctKeys]
            if len(wrongKeys)>0:
                for wrongKey in wrongKeys:
                    self.logger.info(f' * Error: `{wrongKey}` flag not recognised.')
                raise Exception('WrongKeyError')
            
            # removing empty flags
            self.logger.info(f'Removing empty flags from config.', 1)
            keys = list(configs.keys()) # we need this so python does not complain about size change
            for key in keys:
                if configs[key] == None:
                    self.logger.info(f' * {key} deleted.', 2)
                    del configs[key]
            
            self.logger.info(f'Set missing configs with default ones.', 1)
            self.configs = _defaultConfigs | configs
        else:
            self.logger.info(f'Configuration file is absent.', 1)
            self.logger.info(f' * default configuration will be used', 1)
            self.configs = _defaultConfigs
        
        # print configs to logger
        self.logger.info(f'The system configuration is:', 2)
        for k,v in self.configs.items():
            self.logger.info(f' * {k} : {v}', 2)
        

    def get(self, key):
        return self.configs[key]
    

_correctKeys = {
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
    'mpirun_qe',
    'mpirun_w90',
}

_defaultConfigs = {
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
    'mpirun_qe' : 'mpirun',
    'mpirun_w90' : 'mpirun',
}