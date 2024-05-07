import itertools
from qeflow.utils import saveYaml
from qeflow.logger import Logger
import os


def createWorkflow(inp, logger = Logger()):
    '''
    Returns a list of dictionaries. Each dictionary is the input of a specific code in the workflow.
    Also, each dictionary is the cartesian product of the `withrespectto` flag entries.
    '''

    params = []
    valuesList = []
    for wrt in inp['withrespectto']:
        for k, v in wrt.items():
            params.append(k)
            valuesList.append(v)
    #product = [list(p) for p in itertools.product(*valuesList)]
    product = list(itertools.product(*valuesList))

    wrtDicts = []
    for values in product:
        aux = {}
        for k,v in zip(params, values):
            aux[k] = v
        wrtDicts.append(aux)

    data = {}

    print(params)
    print(product)
    for i, par in enumerate(params):
        data[par] = [product[j][i] for j in range(len(product))] #series[:,i]
    print('data: ', data)

    # merging dictionary default | explicit, explicit keys overwrite the default ones
    flowDicts = []
    for work, task in zip(inp['workflow'], inp['tasks']):
        aux = inp | work[task]
        aux = removeKeys(aux, keysToRemove)
        aux['task'] = task
        flowDicts.append(aux)
    
    # merge all dicts together
    logger.info(f'\n--------------------------------', 1)
    logger.info(f'Workflow that will be performed:', 1)
    for task in inp['tasks']:
        logger.info(f' * {task}', 1)
    taskDicts = []
    logger.info(f'Each workflow will iterate {len(wrtDicts)} times.', 1)
    logger.info(f'Iterating parameters:', 1)
    for wrt in wrtDicts:
        logger.info(f' * { wrt }', 1)
        for flow in flowDicts:
            aux = flow | wrt
            taskDicts.append(aux)
    
    for i, task in enumerate(taskDicts):
        task['fileNameIn'] = os.path.join(inp['calc_dir'], f'{i:03d}.in')
        task['fileNameOut'] = os.path.join(inp['calc_dir'], f'{i:03d}.out')
    
    saveYaml(taskDicts, inp['workflow_path'])

    return taskDicts


def removeKeys(d, listKeys):
    for k in listKeys:
        del d[k]
    return d


keysToRemove = [
    'workflow',
    'workflow_path',
    'tasks',
    'withrespectto',
    'nprocs',
    'time',
    'partition',
    'qos',
]

