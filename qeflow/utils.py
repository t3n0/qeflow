
from yaml import safe_load

def readYaml(path):
    '''
    Reads and returns the YAML dictionary.
    '''
    with open(path,'r') as f: 
        data = safe_load(f)
    return data
