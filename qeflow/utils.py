
from yaml import safe_load

def readYaml(path):
    '''
    Reads and returns the YAML dictionary.
    '''
    with open(path,'r') as f: 
        data = safe_load(f)
    return data


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